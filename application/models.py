import uuid
from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
import pymongo
# from application import app

# from functools import wraps
# import jwt

#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.SmartKids


# # decorator for verifying the JWT
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         # jwt is passed in the request header
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         # return 401 if token is not passed
#         if not token:
#             return jsonify({'message' : 'Token is missing !!'}), 401
  
#         try:
#             # decoding the payload to fetch the stored details
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = Parent.query\
#                 .filter_by(public_id = data['public_id'])\
#                 .first()
#         except:
#             return jsonify({
#                 'message' : 'Token is invalid !!'
#             }), 401
#         # returns the current logged in users contex to the routes
#         return  f(current_user, *args, **kwargs)
  
#     return decorated

#Models


class Parent:

    # SignUp
    def signUp(self):
        print(request)

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "user_name": request.json['user_name'],
            "email": request.json['email'],
            "password": request.json['password'],
            "image": "",
            "parentId": "",
            # "parentId": request.json['parentId'],
            "access_token": "",
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
 
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400
        
        user["access_token"] = create_access_token(identity=user['email'])

        db.users.insert_one(user)
        return jsonify({"success":"SignUp successfully", "user": user}), 200


    # SignIn
    def signIn(self):
        user = db.users.find_one({
            "email": request.json['email']
        })
        if user:
            if pbkdf2_sha256.verify(request.json['password'], user['password']):
                user["access_token"] = create_access_token(identity=user['email'])
                filter = {'email': user['email']}
                db.users.update_one(filter, {"$set": {"access_token":user["access_token"]}})
                parent = db.users.find_one({"email": request.json['email']})
                return jsonify({"success":"Login successfully", "user": parent}), 200
            else:
                return jsonify({"error":"Password is not correct" }), 401
        else:
            return jsonify({"error":"Invalid login email" }), 402

    def getParentByEmail(self, email):
        user = db.users.find_one({"email":email})
        return jsonify({"success":"Success", 'user': user }), 200

    #Get user information by token and userId 
    def getParentById(self, token, parentId):
        parent = db.users.find_one({"_id":parentId})
        print(parent)
        if parent['access_token'] == token:
            parent["access_token"] = create_access_token(identity=parent['email'])
            filter = {"_id":parentId}
            db.users.update_one(filter, {"$set": {"access_token":parent["access_token"]}})
            parent = db.users.find_one({"_id":parentId})
            return jsonify({"success":"Success", 'user': parent }), 200
        else:
            return jsonify({"error":"Invalid login" }), 402
        

    def updateParent(self, email):
        user_name=request.json['user_name']
        password=request.json['password']
        image=request.json['image']

        # Encrypt the password
        if (password != ''):
            password = pbkdf2_sha256.encrypt(password)
            db.users.find_one_and_update({"email":email}, {"$set": {"user_name":user_name, "password": password, "image":image}})
        else:
            db.users.find_one_and_update({"email":email}, {"$set": {"user_name":user_name, "image":image}})

        user = db.users.find_one({"email":email})
        return jsonify({"success":"Update user uccessfully", "user": user}), 200


class Child(Parent):

    # create kid for the parent
    def createKid(self, kid_name, parentId, token):
        print(request)
        
        myquery={"$and":[{"parentId":parentId, "user_name":kid_name}]}
        kid = db.users.find_one(myquery)

        if kid:
            return jsonify({"error":"User exitst"}), 400
        else:
        #Create the user object
            kid = {
                "_id": uuid.uuid4().hex,
                "user_name": kid_name,
                "image": "",
                "parentId": parentId,
                "points": 0,
                "access_token": token,
            }
            db.users.insert_one(kid)
            return jsonify({"success":"Kid login successfully", "user": kid}), 200

    def getKidById(self, kidId, token):
        kid = db.users.find_one({"_id":kidId})
        print(kid)
        if kid['access_token'] == token:
            return jsonify({"success":"Success", 'kid': kid }), 200
        else:
            return jsonify({"error":"Invalid login" }), 402
        
    

    # Get kids information for the parent
    def getKidsByParentId(self, parentId):
        users = db.users.find({"parentId":parentId})
        return jsonify({"user":[user for user in users]})

    
    
    def deleteKid(self, kidId):
        kid = db.users.find_one({"_id":kidId})
        if kid:
            db.users.delete_one(kid)
            return jsonify({"success":"Delete successfully"}), 200
        else:
            return jsonify({"error":"User not found"}), 410
 

class Point:
    def updatePoint(self, kidId, points):
        kid = db.users.find_one({"_id":kidId})
        if kid:
            filter = {"_id":kidId}
            db.users.update_one(filter, {"$set": {"points":points}})
        # user = db.users.find_one(myquery)
        user = db.users.find_one({"_id":kidId})
        return jsonify({"success":"Update kid point successfully", "user": user}), 200


    # def updateKid(self, email, kid_name):
    #     parent = db.users.find_one({"email":email})
    #     user_name=request.json['user_name']

    #     print(parent['_id'], kid_name)
    #     image=request.json['image']
    #     myquery={"$and":[{"parentId":parent['_id'], "user_name":kid_name}]}
    #     newvalues={"$set": {"user_name":user_name, "image":image}}
    #     db.users.find_one_and_update(myquery, newvalues)
    #     # user = db.users.find_one(myquery)
    #     user = db.users.find_one({"$or":[{"parentId":parent['_id'], "user_name":user_name}]})
    #     return jsonify({"success":"Update kid successfully", "user": user}), 200


