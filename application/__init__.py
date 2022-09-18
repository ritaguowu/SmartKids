from flask import Flask
from .api.routes import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

#Config JWT token
app.config['JWT_SECRET_KEY'] = '5ad5a0c7ba484ecd968ebe435b26a298'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=30)


jwt = JWTManager(app)

app.register_blueprint(api)


from application import routes