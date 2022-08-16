from flask import Blueprint, request, jsonify
from application.models import Parent, Child

api = Blueprint('api', __name__, url_prefix='/api/v1')

#Routes
@api.route("/parent", methods=['POST'])
def parent():
    return Parent().signup()

@api.route("/auth", methods=['POST'])
def auth():
    return Parent().getToken()

@api.route("/kid",  methods=['POST'])
def kid():
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Parent().signupKid(parentId)

@api.route("/kids",  methods=['GET'])
def kids():
    parentId = request.args.get('parentId')
    if parentId is None:
        return jsonify({"error":"Please provide the parentId" }), 403
    else:
        return Child().getKidsByParentId(parentId)