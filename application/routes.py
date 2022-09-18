from application import app
from application.models import Parent

#Routes
@app.route("/signup", methods=['POST'])
def signup():
    return Parent().signup()

@app.route("/login", methods=['POST'])
def login():
    return Parent().login()
