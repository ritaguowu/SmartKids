from flask import Flask
import pymongo


app = Flask(__name__)


#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.SmartKids

from application import routes