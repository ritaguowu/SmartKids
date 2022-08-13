from flask import Flask
from application import app
from application.models import User

#Routes
@app.route("/signup", methods=['POST'])
def signup():
    return User().signup()


