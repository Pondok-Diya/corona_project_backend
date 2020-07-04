from flask_restful import Resource
from flask import request
from app import app, db
from flask_jwt_extended import jwt_required
from passlib.hash import pbkdf2_sha256 as sha256
import uuid
from datetime import datetime

def stringTime(dt):
    return datetime.strptime(dt,"%Y-%m-%d")

def postBioSiswa(uuid,nama,username,jk,alamat,tempat_lahir,tanggal_lahir,hp,email,now,uuid_siswa):
    sql = """insert into bio_siswa values(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    params = [uuid,nama,username,jk,alamat,tempat_lahir,tanggal_lahir,hp,email,now,now,uuid_siswa]
    return db.commit_data(sql,params)

def postSiswa(uuid_siswa,username,password,now):
    sql = """insert into siswa values(0,%s,%s,%s,%s,%s)"""
    params = [uuid_siswa,username,password,now,now]
    return db.commit_data(sql,params)

class DaftarMateri(Resource):
    @jwt_required
    def get(self):
        sql = """select * from materi"""
        return db.get_data(sql)

class DetailMateri(Resource):
    def get(self,id):
        sql = """select * from materi where uuid = %s"""
        return db.get_one(sql,[id])

class PrfileSiswa(Resource):
    def get(self,id):
        sql = """select * from bio_siswa where uuid_siswa = %s"""
        return db.get_one(sql,[id])

class TambahSiswa(Resource):
    def post(self):
        now = datetime.now()
        data = request.get_json()
        uuid_bio = str(uuid.uuid4())
        uuid_siswa = str(uuid.uuid4())
        password = sha256.hash(data["password"])
        now = datetime.now()
        tanggal_lahir = stringTime(data["tanggal_lahir"])
        postBioSiswa(uuid_bio,data["nama"],data["username"],data["jk"],data["alamat"],data["tempat_lahir"],tanggal_lahir,data["hp"],data["email"],now,uuid_siswa)
        postSiswa(uuid_siswa,data["username"],password,now)