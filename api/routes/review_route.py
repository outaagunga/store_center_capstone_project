
from flask import request, jsonify, make_response, session, redirect
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from collections import OrderedDict
from models.user import User
from models.order import Order
from models.database import db, app
from models.storagespace import StorageSpace
from models.review import Review


# Creating review

@app.route('/review', methods=['POST'])
def create_review():
    if request.method == 'POST':

        user_id = []

        # Get data from the request (validate and sanitize as needed)
        data = request.get_json()
        order_id = data.get('order_id')
        rating = data.get('rating')
        comment = data.get('comment')

        # Check if the user has rights to review this order
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            return jsonify({"message": "Order not found"}), 404

        if order.user_id != user_id:
            return jsonify({"message": "Unauthorized to review this order"}), 403

        # Create a new review instance
        review = Review(user_id=user_id, order_id=order_id,
                        rating=rating, comment=comment)

        # Add the review to the database
        db.session.add(review)
        db.session.commit()

        return jsonify({"message": "Review created successfully"}), 201
    else:
        return jsonify({"message": "Invalid request method"}), 405

# Get all reviews


@app.route('/reviews', methods=['GET'])
def get_reviews():
    if request.method == 'GET':
        # Query the database to get all reviews
        reviews = Review.query.all()

        # Serialize the reviews to JSON format (you might want to use a library like Flask-RESTful)
        serialized_reviews = []

        for review in reviews:
            serialized_review = {
                'user_id': review.user_id,
                'order_id': review.order_id,
                'rating': review.rating,
                'comment': review.comment
            }
            serialized_reviews.append(serialized_review)

        return jsonify(serialized_reviews), 200
    else:
        return jsonify({"message": "Invalid request method"}), 405
