from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/SignUP"

mongo = PyMongo(app)



@app.route('/signup', methods=['POST'])
def signup():
    _json = request.json
    _username = _json['username']
    _email = _json['email']
    _pwd = _json['pwd']

    if _username and _email and _pwd and request.method == "POST":
        hashpwd = generate_password_hash(_pwd)
        mongo.db.user.insert(
            {'name': _username, 'email': _email, 'password': hashpwd})
        return jsonify("user info added")
    return jsonify("not corekt")

@app.route('/')
def users():
    result = mongo.db.user.find()
    return dumps(result)

@app.route('/signin/<username>/<password>',methods=['GET'])
def signin(username,password):
     dbpassword= mongo.db.user.find_one({'name':username})['password']
     result=check_password_hash(dbpassword,password)
     return str(result)


if __name__ == "__main__":
    app.run(debug=True)
