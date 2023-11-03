# app.py
from flask import jsonify, request
from flask import jsonify
from flask import Flask, request, jsonify, make_response, session
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'opuyoapuga'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storecenter.db'

db.init_app(app)
migrate = Migrate(app, db)


# Home Page
@app.route('/')
def home():
    return "Welcome to Jeco API"

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


# Getting all users


# @app.route('/users', methods=['GET'])
# @token_required
# def get_all_users(user):
#     # Check if the user has the appropriate permissions.
#     if not user.role == 'admin':
#         return jsonify({'message': 'You are not allowed to perform that action'})

#     # Get all users from the database.
#     try:
#         users = User.query.all()
#     except Exception as e:
#         return jsonify({'error': str(e)})

#     # Create a list of user data dictionaries.
#     user_list = []
#     for user in users:
#         user_data = {
#             'id': user.user_id,
#             'public_id': user.public_id,
#             'username': user.username,
#             'email': user.email,
#             'role': user.role,
#             'bookings': [],
#             'storage_units': []
#         }

#         # Get all bookings for the user.
#         try:
#             bookings = user.bookings
#         except Exception as e:
#             return jsonify({'error': str(e)})

#             # Add the booking data to the user data dictionary.
#         for booking in bookings:
#             booking_data = {
#                 'id': booking.id,
#                 'start_date': booking.start_date.isoformat(),
#                 'end_date': booking.end_date.isoformat(),
#                 'pickup_requested': booking.pickup_requested,
#                 'delivery_requested': booking.delivery_requested
#             }
#             user_data['bookings'].append(booking_data)

#         # Get all storage units for the user.
#         try:
#             storage_units = user.storage_units
#         except Exception as e:
#             return jsonify({'error': str(e)})

#         # Add the storage unit data to the user data dictionary.
#         for storage_unit in storage_units:
#             storage_unit_data = {
#                 'id': storage_unit.id,
#                 'unit_name': storage_unit.unit_name,
#                 'price': storage_unit.price
#             }
#             user_data['storage_units'].append(storage_unit_data)

#         user_list.append(user_data)

#     return jsonify({'users': user_list})


# # Signup
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         # Create a new User record for the client
#         new_user = User(username=username, email=email,
#                         password=password, role='client')

#         # Add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()

#         # Redirect to the login page or a success page
#         return redirect('/login')

#     return render_template('signup.html')


# Get all users and all their data
# @app.route('/users', methods=['GET'])
# @token_required
# def get_all_users(user):
#     # Check if the user has the appropriate permissions.
#     if not user.role == 'admin':
#         return jsonify({'message': 'You are not allowed to perform that action'}), 403

#     try:
#         # Query all users, their associated orders, and storage units in a single database query
#         users = User.query.all()

#         # Create a list of user data dictionaries
#         user_list = []
#         for user in users:
#             user_data = {
#                 'id': user.user_id,
#                 'public_id': user.public_id,
#                 'full_name': user.full_name,
#                 'username': user.username,
#                 'email': user.email,
#                 'role': user.role,
#                 'bookings': [],
#                 'storage_units': []
#             }

#             # Extract user's orders
#             orders = user.orders
#             for order in orders:
#                 order_data = {
#                     'id': order.id,
#                     'order_date': order.order_date.isoformat(),
#                     'delivery_date': order.delivery_date.isoformat(),
#                     'total_price': order.total_price,
#                     'payment_status': order.payment_status,
#                     'order_reference_code': order.order_reference_code,
#                     'packed': order.packed
#                     # Add more fields as needed
#                 }
#                 user_data['bookings'].append(order_data)

#             # Extract user's storage units
#             customer = user.customers[0]  # Assuming one customer per user
#             storage_units = customer.orders
#             for storage_unit in storage_units:
#                 storage_unit_data = {
#                     'id': storage_unit.storage_space.id,
#                     'size': storage_unit.storage_space.size,
#                     'price': storage_unit.storage_space.price,
#                 }
#                 user_data['storage_units'].append(storage_unit_data)

#             user_list.append(user_data)

#         return jsonify({'users': user_list})

#     except Exception as e:
#         return jsonify({'error': str(e)})

#Getting all users
@app.route('/users', methods=['GET'])
# @token_required
def get_all_users():
    # Check if the user has the appropriate permissions.
    # if not user.role == 'admin':
    #     return jsonify({'message': 'You are not allowed to perform that action'}), 403

    try:
        # Query all users in a single database query
        users = User.query.all()

        # Create a list of user data dictionaries
        user_list = []
        for user in users:
            user_data = {
                'id': user.user_id,
                'public_id': user.public_id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'bookings': [],
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
                    'payment_status': order.payment_status,
                    'order_reference_code': order.order_reference_code,
                    'packed': order.packed
                    # Add more fields as needed
                }
                user_data['bookings'].append(order_data)

            # Extract user's storage units (assuming one customer per user)
            customer = user.customer  # Get the customer associated with the user
            if customer:
                storage_units = customer.storage_units
                for storage_unit in storage_units:
                    storage_unit_data = {
                        'id': storage_unit.id,
                        'size': storage_unit.size,
                        'price': storage_unit.price,
                    }
                    user_data['storage_units'].append(storage_unit_data)

            user_list.append(user_data)

        return jsonify({'users': user_list})

    except Exception as e:
        return jsonify({'error': str(e)})

# Getting a single user
@app.route('/users/<int:user_id>', methods=['GET'])
# @token_required
def get_single_user(user_id):
    try:
        # Query the database to find the user with the specified user_id
        user = User.query.get(user_id)

        if user:
            # Create a user data dictionary
            user_data = {
                'id': user.user_id,
                'public_id': user.public_id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'bookings': [],
                'storage_units': []
            }

            # Extract user's orders
            for order in user.orders:
                order_data = {
                    'id': order.id,
                    'order_date': order.order_date.isoformat(),
                    'delivery_date': order.delivery_date.isoformat(),
                    'total_price': order.total_price,
                    'payment_status': order.payment_status,
                    'order_reference_code': order.order_reference_code,
                    'packed': order.packed
                    # Add more fields as needed
                }
                user_data['bookings'].append(order_data)

            # Extract user's storage units (assuming one customer per user)
            customer = user.customer  # Get the customer associated with the user
            if customer:
                for storage_unit in customer.storage_units:
                    storage_unit_data = {
                        'id': storage_unit.id,
                        'size': storage_unit.size,
                        'price': storage_unit.price,
                    }
                    user_data['storage_units'].append(storage_unit_data)

            return jsonify({'user': user_data})
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)})


# Creating a user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    existing_user = User.query.filter_by(username=data['username']).first()
    existing_email = User.query.filter_by(email=data['email']).first()

    if existing_user:
        return jsonify({'error': 'Username is already taken'}), 409

    if existing_email:
        return jsonify({'error': 'Email is already in use'}), 409

    try:
        hashed_password = generate_password_hash(
            data['password'], method='pbkdf2:sha256')

        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            password=hashed_password,
            role=data['role'],
            profile_picture=data.get('profile_picture'),  # Include profile_picture if present
            address=data.get('address')  # Include address if present
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User creation failed. Please try again later.'}), 500

# Updating existing user
@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Retrieve the user from the database based on the user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if the username and email are being updated
    if 'username' in data:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.user_id != user.user_id:
            return jsonify({'error': 'Username is already taken'}), 409

    if 'email' in data:
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email and existing_email.user_id != user.user_id:
            return jsonify({'error': 'Email is already in use'}), 409

    try:
        # Update user data
        if 'password' in data:
            hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
            user.password = hashed_password

        if 'username' in data:
            user.username = data['username']

        if 'email' in data:
            user.email = data['email']

        if 'full_name' in data:
            user.full_name = data['full_name']

        if 'phone_number' in data:
            user.phone_number = data['phone_number']

        if 'role' in data:
            user.role = data['role']

        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']

        if 'address' in data:
            user.address = data['address']

        db.session.commit()

        # After successfully updating the user, return the updated user data
        updated_user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'phone_number': user.phone_number,
            'role': user.role,
            'profile_picture': user.profile_picture,
            'address': user.address
        }

        return jsonify({'message': 'User updated successfully', 'user': updated_user_data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User update failed. Please try again later.'}), 500




if __name__ == '__main__':
    app.run(debug=True)
