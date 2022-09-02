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
@api.route('/user', methods=['GET'])
def getUser():
    token = request.args.get('token', None)
    print(token)
    parentId = request.args.get('parentId', None)
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Parent().getUserById(token, parentId)


# Get kids information for the parent
@api.route("/kids",  methods=['GET'])
@jwt_required()
def getKids():
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Child().getKidsByParentId(parentId)

# Add kid for the parent
@api.route("/kid",  methods=['POST'])
@jwt_required()
def addKid():
    kid_name = request.args.get('kidName')
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Child().createKid(kid_name, parentId)

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


@api.route('/kid', methods=['DELETE'])
def removeKid():
    kidId = request.args.get('kidId')
    # if None in (email, kid_name):
    if kidId is None:
        return jsonify({"error":"Please provide the kid's id" }), 409
    else:
        return Child().deleteKid(kidId)


# @api.route('/user', methods=['GET'])
# @jwt_required()
# def getUser():
#     token = request.headers["Authorization"].split(" ")[1]
#     print(token)
#     parentId = request.args.get('parentId')
#     if parentId is None:
#         return jsonify({"error":"Please provide the parentId" }), 403
#     else:
#         return Parent().getUserById(token, parentId)




@api.route('/parent', methods=['GET'])
def getParent():
    email = request.args.get('email') 
    if email is None:
        return jsonify({"error":"Please provide the email" }), 410
    else:
        return Parent().getParentByEmail(email)


@api.route('/kid', methods=['PUT'])
def updateKid():
    email = request.args.get('email')
    kid_name = request.args.get('kid_name')
    if None in (email, kid_name):
        return jsonify({"error":"Please provide the user email and kid's name" }), 409
    else:
        return Child().updateKid(email, kid_name)

