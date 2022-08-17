from flask import Blueprint, request, jsonify
from application.models import Parent, Child

api = Blueprint('api', __name__, url_prefix='/api/v1')

#Routes
@api.route("/parent", methods=['POST'])
def signup():
    return Parent().signup()

@api.route("/auth", methods=['POST'])
def auth():
    return Parent().getToken()

@api.route("/kid",  methods=['POST'])
def addKid():
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Child().signupKid(parentId)

@api.route("/kids",  methods=['GET'])
def getKids():
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Child().getKidsByParentId(parentId)

@api.route('/parent', methods=['GET'])
def getParent():
    email = request.args.get('email') 
    if email is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Parent().getParent(email)


@api.route('/parent', methods=['PUT'])
def updateParent():
    email = request.args.get('email') 
    if email is None:
        return jsonify({"error":"Please provide the user email" }), 403
    else:
        return Parent().updateParent(email)

@api.route('kid', methods=['PUT'])
def updateKid():
    email = request.args.get('email')
    kid_name = request.args.get('kid_name')
    if None in (email, kid_name):
        return jsonify({"error":"Please provide the user email and kid's name" }), 409
    else:
        return Child().updateKid(email, kid_name)

@api.route('kid', methods=['DELETE'])
def deleteKid():
    email = request.args.get('email')
    kid_name = request.args.get('kid_name')
    if None in (email, kid_name):
        return jsonify({"error":"Please provide the user email and kid's name" }), 409
    else:
        return Child().deleteKid(email, kid_name)