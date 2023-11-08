from collections import OrderedDict
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from models.user import User
from models.order import Order
from models.database import db, app
from models.storagespace import StorageSpace
from models.review import Review


# Getting all users
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        # Query all users
        users = User.query.all()

        # Create a list to store user data dictionaries
        user_list = []

        for user in users:
            # Create a user data dictionary
            user_data = {
                'user_id': user.user_id,
                'public_id': user.public_id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'profile_picture': user.profile_picture,
                'address': user.address,
                'role': user.role,
                'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
                'gender': user.gender,
                'bio': user.bio,
                'orders': [],
                'storage_units': []
            }

            # Extract user's orders
            orders = user.orders
            for order in orders:
                order_data = {
                    'id': order.id,
                    'order_date': order.order_date.isoformat(),
                    'delivery_date': order.delivery_date.isoformat(),
                    'total_price': order.total_price,
                    'number_of_items': order.number_of_items,
                    'invoice': order.invoice,
                    'payment_method': order.payment_method,
                    'booking_date': order.booking_date.isoformat(),
                    'booking_status': order.booking_status,
                    'payment_status': order.payment_status,
                    'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                    'pickup_date_actual': order.pickup_date_actual.isoformat(),
                    'order_reference_code': order.order_reference_code,
                    'packed': order.packed,
                    'shipment_status': order.shipment_status,
                    'shipment_tracking_number': order.shipment_tracking_number,
                    'shipment_carrier': order.shipment_carrier,
                    'shipment_eta': order.shipment_eta.isoformat() if order.shipment_eta else None
                }
                user_data['orders'].append(order_data)

            # Extract user's storage units (if they exist)
            if hasattr(user, 'storage_units'):
                storage_units = user.storage_units
                for storage_unit in storage_units:
                    storage_unit_data = {
                        'id': storage_unit.id,
                        'name': storage_unit.name,
                        'description': storage_unit.description,
                        'size': storage_unit.size,
                        'capacity': storage_unit.capacity,
                        'price_per_month': storage_unit.price_per_month,
                        'available': storage_unit.available,
                        'address': storage_unit.address,
                        'latitude': storage_unit.latitude,
                        'longitude': storage_unit.longitude
                    }
                    user_data['storage_units'].append(storage_unit_data)

            user_list.append(user_data)

        # Return the user data list as JSON
        return jsonify({'users': user_list})

    except Exception as e:
        return jsonify({'error': str(e)})


# Route to get single user
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Find the user by user ID
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Create a user data dictionary
        user_data = {
            'user_id': user.user_id,
            'public_id': user.public_id,
            'full_name': user.full_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'profile_picture': user.profile_picture,
            'address': user.address,
            'role': user.role,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'gender': user.gender,
            'bio': user.bio,
            'orders': [],
            'storage_units': []
        }

        # Extract user's orders
        orders = user.orders
        for order in orders:
            order_data = {
                'id': order.id,
                'order_date': order.order_date.isoformat(),
                'delivery_date': order.delivery_date.isoformat(),
                'total_price': order.total_price,
                'number_of_items': order.number_of_items,
                'invoice': order.invoice,
                'payment_method': order.payment_method,
                'booking_date': order.booking_date.isoformat(),
                'booking_status': order.booking_status,
                'payment_status': order.payment_status,
                'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                'pickup_date_actual': order.pickup_date_actual.isoformat(),
                'order_reference_code': order.order_reference_code,
                'packed': order.packed,
                'shipment_status': order.shipment_status,
                'shipment_tracking_number': order.shipment_tracking_number,
                'shipment_carrier': order.shipment_carrier,
                'shipment_eta': order.shipment_eta.isoformat() if order.shipment_eta else None
            }
            user_data['orders'].append(order_data)

        # Extract user's storage units (if they exist)
        if hasattr(user, 'storage_units'):
            storage_units = user.storage_units
            for storage_unit in storage_units:
                storage_unit_data = {
                    'id': storage_unit.id,
                    'name': storage_unit.name,
                    'description': storage_unit.description,
                    'size': storage_unit.size,
                    'capacity': storage_unit.capacity,
                    'price_per_month': storage_unit.price_per_month,
                    'available': storage_unit.available,
                    'address': storage_unit.address,
                    'latitude': storage_unit.latitude,
                    'longitude': storage_unit.longitude
                }
                user_data['storage_units'].append(storage_unit_data)

        # Return the user data as JSON
        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)})


#  Creating a user
@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # Check if required fields are provided in the request
        required_fields = ['username', 'email', 'password',
                           'full_name', 'phone_number', 'role']
        for field in required_fields:
            if field not in data:

                return jsonify({'error': f'Missing field: {field}'}), 400

        # Check if the username and email are already in use
        existing_user = User.query.filter_by(username=data['username']).first()
        existing_email = User.query.filter_by(email=data['email']).first()
        existing_phone = User.query.filter_by(
            phone_number=data['phone_number']).first()

        if existing_user:
            return jsonify({'error': 'Username is already taken'}), 409

        if existing_email:
            # Print the email that is already in use
            print(f"Email '{data['email']}' is already in use")
            return jsonify({'error': 'Email is already in use'}), 409

        if existing_phone:
            # Print the phone number that is already in use
            print(f"Phone number '{data['phone_number']}' is already in use")
            return jsonify({'error': 'Phone number is already in use'}), 409

        # Hash the password
        hashed_password = generate_password_hash(
            data['password'], method='pbkdf2:sha256')

        # Parse and convert the date_of_birth string to a Python date object
        date_of_birth_str = data.get('date_of_birth')
        date_of_birth = None

        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(
                    date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format here, e.g., return an error response
                return jsonify({'error': 'Invalid date_of birth format. Please use YYYY-MM-DD'}), 400

        # Create a new user with all fields, including the date_of_birth
        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            password=hashed_password,
            role=data['role'],
            profile_picture=data.get('profile_picture'),
            address=data.get('address'),
            date_of_birth=date_of_birth,  # Use the parsed date_of_birth
            gender=data.get('gender'),
            bio=data.get('bio')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})
    except Exception as e:
        # Print the exception for troubleshooting
        print("Exception:", e)

        db.session.rollback()
        return jsonify({'error': 'User creation failed. Please try again later.'}), 500


# Deleting a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
# @token_required
def delete_user(user_id):
    try:
        # Query the user by user_id
        user = User.query.get(user_id)

        if user is not None:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'User deleted successfully'})

        return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)})


# Updating a user details:
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Retrieve the user from the database based on the user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        if 'full_name' in data:
            user.full_name = data['full_name']

        if 'username' in data:
            # Check for a unique username
            existing_user = User.query.filter_by(
                username=data['username']).first()
            if existing_user and existing_user.user_id != user.user_id:
                return jsonify({'error': 'Username is already taken'}), 409
            user.username = data['username']

        if 'email' in data:
            # Check for a unique email
            existing_email = User.query.filter_by(email=data['email']).first()
            if existing_email and existing_email.user_id != user.user_id:
                return jsonify({'error': 'Email is already in use'}), 409
            user.email = data['email']

        if 'phone_number' in data:
            user.phone_number = data['phone_number']

        if 'role' in data:
            user.role = data['role']

        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']

        if 'address' in data:
            user.address = data['address']

        if 'bio' in data:
            user.bio = data['bio']

        if 'password' in data:
            # password hashed
            hashed_password = generate_password_hash(
                data['password'], method='pbkdf2:sha256')
            user.password = hashed_password

        if 'date_of_birth' in data:
            # Parse and convert the date_of_birth string to a Python date object
            date_of_birth_str = data['date_of_birth']
            date_of_birth = None

            if date_of_birth_str:
                try:
                    date_of_birth = datetime.strptime(
                        date_of_birth_str, '%Y-%m-%d').date()
                except ValueError:
                    # Handle invalid date format here, e.g., return an error response
                    return jsonify({'error': 'Invalid date of birth format. Please use YYYY-MM-DD'}), 400

            user.date_of_birth = date_of_birth

        if 'gender' in data:
            user.gender = data['gender']

        db.session.commit()

        updated_user_data = {
            'user_id': user.user_id,
            'full_name': user.full_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
            'profile_picture': user.profile_picture,
            'address': user.address,
            'bio': user.bio,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
            'gender': user.gender,
        }

        return jsonify({'message': 'User updated successfully', 'user': updated_user_data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User update failed. Please try again later.'}), 500
