from functools import wraps
from flask import Blueprint, request, jsonify
from models.users import User
from models.dbconfig import db
from config import Config
import jwt

user_routes = Blueprint('users', __name__)

config = Config()
SECRET_KEY = config.SECRET_KEY



def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 403
            try:
                data = jwt.decode(token, SECRET_KEY)
                user_id = data['user_id']
                user = User.query.filter_by(id=user_id).first()
                if user.role not in roles:
                    return jsonify({'message': 'Access denied!'}), 403
            except:
                return jsonify({'message': 'Token is invalid!'}), 403
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@user_routes.route('/profile', methods=['GET'])
@requires_roles('admin', 'client', 'employee')
def get_profile():
    token = request.headers.get('Authorization')
    data = jwt.decode(token, SECRET_KEY)
    user_id = data['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    return jsonify(user.to_dict()), 200

@user_routes.route('/profile', methods=['PUT'])
@requires_roles('admin', 'client', 'employee')
def update_profile():
    token = request.headers.get('Authorization')
    data = jwt.decode(token, SECRET_KEY)
    user_id = data['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    
    # Assuming you've passed updated data as JSON in the request
    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.profile_image_url = data.get('profile_image_url', user.profile_image_url)

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully!'}), 200

@user_routes.route('/users', methods=['GET'])
@requires_roles('admin')
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
@requires_roles('admin')
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200

@user_routes.route('/users/<int:user_id>/assign-role', methods=['PUT'])
@requires_roles('admin')
def assign_role(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    data = request.get_json()
    new_role = data.get('role')
    if new_role not in ['admin', 'client', 'employee']:
        return jsonify({'message': 'Invalid role!'}), 400

    user.user_type = new_role
    db.session.commit()
    return jsonify({'message': 'Role assigned successfully!'}), 200