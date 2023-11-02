from functools import wraps
from flask import Blueprint, request, jsonify
from models.users import User
from models.booking import Booking
from datetime import datetime
from models.dbconfig import db
from config import Config
import jwt




booking_routes =Blueprint('booking', __name__)


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


@booking_routes.route('/create', methods=['POST'])
@requires_roles('client', 'admin')
def create_booking():
    data = request.get_json()
    
    client_id = data['client_id']
    unit_id = data['unit_id']
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
    product_id = data['product_id']
    
    new_booking = Booking(client_id=client_id, unit_id=unit_id, start_date=start_date, end_date=end_date, product_id=product_id)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully!'}), 201

@booking_routes.route('/<int:booking_id>', methods=['GET'])
@requires_roles('client', 'employee', 'admin')
def view_booking(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    
    # For simplicity, the same serialized data is being returned to all roles.
    return jsonify(booking.to_dict()), 200


@booking_routes.route('/update/<int:booking_id>', methods=['PUT'])
@requires_roles('client', 'admin')
def update_booking(booking_id):
    data = request.get_json()
    booking = Booking.query.filter_by(booking_id=booking_id).first()

    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    # Update fields
    booking.start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date() if 'start_date' in data else booking.start_date
    booking.end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date() if 'end_date' in data else booking.end_date
    booking.product_id = data['product_id'] if 'product_id' in data else booking.product_id
    db.session.commit()

    return jsonify({'message': 'Booking updated successfully!'}), 200


@booking_routes.route('/cancel/<int:booking_id>', methods=['DELETE'])
@requires_roles('client', 'admin')
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()

    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    # Check if the booking belongs to the current client 
    token = request.headers.get('Authorization')
    data = jwt.decode(token, SECRET_KEY)
    user_id = data['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    if user.user_type == 'client' and user.user_id != booking.client_id:
        return jsonify({'message': 'Not authorized to cancel this booking'}), 403

    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking cancelled successfully!'}), 200


@booking_routes.route('/assign/<int:booking_id>', methods=['PUT'])
@requires_roles('admin')
def assign_booking(booking_id):
    data = request.get_json()
    booking = Booking.query.filter_by(booking_id=booking_id).first()

    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    employee_id = data['employee_id']
    employee = User.query.filter_by(user_id=employee_id, user_type='employee').first()

    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    # Assuming you have an employee_id field or a similar relation in the Booking model
    booking.employee_id = employee_id
    db.session.commit()

    return jsonify({'message': 'Booking assigned successfully!'}), 200
