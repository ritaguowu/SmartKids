from flask import Blueprint, request, jsonify
from application.models import Parent, Child
from flask_jwt_extended import jwt_required


api = Blueprint('api', __name__, url_prefix='/api/v1')



#Routes

#SignUp
@api.route("/parent", methods=['POST'])
def signup():
    return Parent().signUp()

# SignIn
@api.route("/auth", methods=['POST'])
def auth():
    return Parent().signIn()

#Get user information by token and parentId. For the auto login purpose.
@api.route('/parent', methods=['GET'])
def getParentById():
    token = request.args.get('token', None)
    parentId = request.args.get('parentId', None)
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Parent().getParentById(token, parentId)


# Get kids information for the parent
@api.route("/kids",  methods=['GET'])
@jwt_required()
def getKids():
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Child().getKidsByParentId(parentId)

#Update the parent information
@api.route('/parent', methods=['PUT'])
@jwt_required()
def updateParent():
    email = request.args.get('email') 
    print(email)
    if email is None:
        return jsonify({"error":"Please provide the user email" }), 410
    else:
        return Parent().updateParent(email)


# Add kid for the parent
@api.route("/kid",  methods=['POST'])
@jwt_required()
def addKid():
    kid_name = request.args.get('kidName')
    parentId = request.args.get('parentId')
    token = request.headers["Authorization"].split(" ")[1]
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        if kid_name is None:
           return jsonify({"error":"Please provide the kidName" }), 403 
        else:
            return Child().createKid(kid_name, parentId, token)


# Delete kid for the parent
@api.route('/kid', methods=['DELETE'])
@jwt_required()
def removeKid():
    kidId = request.args.get('kidId')
    token = request.headers["Authorization"].split(" ")[1]
    # if None in (email, kid_name):
    if kidId is None:
        return jsonify({"error":"Please provide the kid's id" }), 409
    else:
        return Child().deleteKid(kidId, token)


#Get one kid information for the parent
@api.route('/kid', methods=['GET'])
@jwt_required()
def getKidById():
    token = request.headers["Authorization"].split(" ")[1]
    print(token)
    kidId = request.args.get('kidId')
    if kidId is None:
        return jsonify({"error":"Please provide the kidId" }), 403
    else:
        return Child().getKidById(kidId, token)


#Update one kid information
@api.route('/kid', methods=['PUT'])
def updateKid():
    kidId = request.args.get('kidId')
    token = request.headers["Authorization"].split(" ")[1]
    print("token:", token)
    # if None in (email, kid_name):
    if kidId is None:
        return jsonify({"error":"Please provide the kid's id" }), 409
    else:
        return Child().updateKid(kidId, token)


@api.route('/parentByEmail', methods=['GET'])
def getParent():
    email = request.args.get('email') 
    if email is None:
        return jsonify({"error":"Please provide the email" }), 410
    else:
        return Parent().getParentByEmail(email)



