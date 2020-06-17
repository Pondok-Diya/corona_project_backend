from flask_restful import Resource
from flask import request
from app import app, db
from flask_jwt_extended import jwt_required
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
import uuid

def stringTime(dt):
    return datetime.strptime(dt,"%Y-%m-%d")

class Materi(Resource):
    @jwt_required
    def get(self):
        return {
            "materi" : "dasar-dasar programing"
        }

class Admin(Resource):
    @jwt_required
    def get(self):
        sql = "select * from user"
        return db.get_data(sql)

class TambahAdmin(Resource):
    def post(self):
        now = datetime.now()
        data = request.get_json()
        sql = """insert into bio_user values(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = [str(uuid.uuid4()),data["nama"],data["username"],sha256.hash(data["password"]),data["superadmin"],data["alamat"],data["tempat_lahir"],stringTime(data["tanggal_lahir"]),data["hp"],data["email"],now,now,str(uuid.uuid4())]
        return db.commit_data(sql,params)
class Siswa(Resource):
    @jwt_required
    def get(self):
        sql = "select * from siswa"
        return db.get_data(sql)
