from application import db
import uuid
from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256

#Models
class User:
    def signup(self):
        print(request)

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "user_name": request.json['user_name'],
            "email": request.json['email'],
            "password": request.json['password'],
            "image": request.json['image'],
            "parentId": request.json['parentId'],
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
 
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        db.users.insert_one(user)
        return jsonify(user), 200

