from flask_restful import Resource
from flask import request
from app import app, db
from flask_jwt_extended import jwt_required
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from app.middleware import superAdmin, admin
import uuid


class Kelas(Resource):
    @jwt_required
    @admin()
    def get(self, uuid_user):
        if uuid_user == "admin":
            sql = """select kelas, label, uuid from kelas"""
            res = db.get_data(sql)
        else:
            sql = """select kelas, label, uuid from pengampu join kelas on pengampu.uuid_kelas = kelas.uuid where uuid_user = %s"""
            res = db.get_data(sql, [uuid_user])
        for i in res:
            i["text"] = str(i["kelas"])+" "+i["label"]
            i["value"] = i["uuid"]
            del i["label"]
            del i["uuid"]
            del i["kelas"]
        return res


class DaftarKelas(Resource):
    @jwt_required
    @superAdmin()
    def get(self):
        sql = """select distinct kelas from kelas"""
        return db.get_data(sql)


class DaftarKelasLabel(Resource):
    @jwt_required
    @superAdmin()
    def get(self, kelas):
        sql = """select uuid, kelas, label from kelas where kelas = %s"""
        return db.get_data(sql, [kelas])


class TambahKelas(Resource):
    @jwt_required
    @superAdmin()
    def post(self):
        data = request.get_json()
        uuid_kelas = str(uuid.uuid4())
        sql = """insert into kelas values(0,%s, %s, %s)"""
        db.commit_data(sql, [uuid_kelas, data["kelas"], data["label"]])


class UpdateKelas(Resource):
    @jwt_required
    @superAdmin()
    def get(self, uuid_kelas):
        sql = """select * from kelas where uuid = %s"""
        return db.get_one(sql, [uuid_kelas])

    @jwt_required
    @superAdmin()
    def put(self, uuid_kelas):
        data = request.get_json()
        sql = """update kelas set kelas = %s, label = %s where uuid = %s"""
        db.commit_data(sql, [data["kelas"], data["label"], uuid_kelas])


class DeleteKelas(Resource):
    @jwt_required
    @superAdmin()
    def delete(self, uuid_kelas):
        sql = """delete from kelas where uuid = %s"""
        db.commit_data(sql, [uuid_kelas])
