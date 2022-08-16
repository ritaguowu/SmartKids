import uuid
from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import pymongo

#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.SmartKids

#Models
class Parent:
    def signup(self):
        print(request)

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "user_name": request.json['user_name'],
            "email": request.json['email'],
            "password": request.json['password'],
            "image": request.json['image'],
            "parentId": "",
            # "parentId": request.json['parentId'],
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
 
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        db.users.insert_one(user)
        return jsonify(user), 200

    def signupKid(self, parentId):
        print(request)

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "user_name": request.json['user_name'],
            "image": request.json['image'],
            "parentId": parentId,
        }

        db.users.insert_one(user)
        return jsonify(user), 200
    

    def getToken(self):
        user = db.users.find_one({
            "email": request.json['email']
        })
        if user:
            if pbkdf2_sha256.verify(request.json['password'], user['password']):
                access_token = create_access_token(identity=user['email'])
                return jsonify({"success":"Login successfully", 'access_token': access_token }), 200
            else:
                return jsonify({"error":"Password is not correct" }), 401
        else:
            return jsonify({"error":"Invalid login email" }), 402


class Child(Parent):
    def getKidsByParentId(self, parentId):
        users = db.users.find({"parentId":parentId})
        return jsonify([user for user in users])