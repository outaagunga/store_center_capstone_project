from functools import wraps
from flask import Blueprint, request, jsonify
from models.users import User
from models.review import Review
from models.dbconfig import db
from config import Config
import jwt



review_routes =Blueprint('reviews', __name__)


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



# Everyone can view reviews
@review_routes.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200


# Only clients can add reviews
@review_routes.route('/add', methods=['POST'])
@requires_roles('client')
def add_review():
    data = request.get_json()
    user_id = jwt.decode(request.headers.get('Authorization'), SECRET_KEY)['user_id']
    review = Review(user_id=user_id, **data)
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully!'}), 201


# Clients can only delete their reviews
@review_routes.route('/delete/<int:review_id>', methods=['DELETE'])
@requires_roles('client')
def delete_review(review_id):
    review = Review.query.filter_by(review_id=review_id).first()

    if not review:
        return jsonify({'message': 'Review not found'}), 404

    token = request.headers.get('Authorization')
    user_id = jwt.decode(token, SECRET_KEY)['user_id']

    # Ensure the review belongs to the logged-in client
    if review.user_id != user_id:
        return jsonify({'message': 'Not authorized to delete this review'}), 403

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully!'}), 200


