# app.py
# from flask import jsonify, request
from flask import Flask, request, jsonify, make_response, session
# import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.user import User
from models.database import db, app


# Decorator that defines @token_required


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        print("Token in decorator:", token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[
                              'HS256'], verify=True)
            print("Decoded token data:", data)
            user = User.query.filter_by(
                user_id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
            print('Token has expired!')
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            print('Token is invalid!')
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(user, *args, **kwargs)

    return decorated


# Login route

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        print("Login failed: Missing or invalid credentials")
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        print("Login failed: User not found")
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id': user.user_id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm='HS256')

        # Decode the token to a string for JSON response
        return jsonify({'token': token})
    print("Login failed: Password check failed")

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
