"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/test')
def test():
    es_divisible_por_dos = lambda numero: True if numero % 2 == 0 else False
    for i in range(1, 101):
        new_user = User(
            email= f"ejemplo{i}",
            password= f"ejemplo{i}",
            is_active= es_divisible_por_dos(i)
        )
        db.session.add(new_user)
    db.session.commit() 
    
    Users = User.query.all()
    return jsonify([user.serialize() for user in Users]), 201


@api.route('/Users')
def getUsers():
    Users = User.query.all()
    return jsonify([user.serialize() for user in Users]), 201

@api.route('/User/Register', methods=['POST'])
def addUser():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    is_active = data.get("is_active")
    
    
    if email is None or email is "":
        return jsonify({"Mensaje": "The email is missing"}), 400
    elif password is None or password is "":
        return jsonify({"Mensaje": "The password is missing"}), 400
    elif is_active is None or is_active is "":
        return jsonify({"Mensaje": "The is_active is missing"}), 400
    try:
        new_user = User(
            email= data.get("email"),
            password= data.get("password"),
            is_active=data.get("is_active")
        )
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(identity=data.get('id'))
        return jsonify({"mensaje": 'Usuario Agregado',"token" : access_token}), 201    
    except Exception as e:
        return jsonify({"error": str(e)}), 400         

@api.route('/User/<user_id>')
def get_user(user_id):
    if user_id is None:
        return jsonify({"Mensaje": "invalid user_id"}), 400
    try:
        user = User.query.filter_by(id=user_id).first()
        return jsonify(user.serialize()), 201  
    except Exception as e:
        return jsonify({"error": str(e)}), 400         

@api.route('/User/Login', methods=['POST'])
def user_autentication():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if email is None or email is "":
        return jsonify({"Mensaje": "The email is missing"}), 400
    elif password is None or password is "":
        return jsonify({"Mensaje": "The password is missing"}), 400
    try:
        user = User.query.filter_by(password=password, email=email).first()
        
        access_token = create_access_token(identity=data.get('id'))
        if user is None:
            return jsonify({"mensaje": "Invalid password or email"}), 400  
        else:
            return jsonify({"Usuario Identificado": user.serialize(),"token" : access_token}), 201    
    except Exception as e:
        return jsonify({"error": str(e)}), 400         

    
    