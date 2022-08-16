from flask import Flask
from .api.routes import api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

#Config JWT token
app.config['JWT_SECRET_KEY'] = '5ad5a0c7ba484ecd968ebe435b26a298'
jwt = JWTManager(app)

app.register_blueprint(api)


from application import routes