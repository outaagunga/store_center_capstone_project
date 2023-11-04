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
from models import db, User, Order

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


# Getting all users
@app.route('/users', methods=['GET'])
# @token_required
def get_all_users():
    try:

        # Query all users
        users = User.query.all()

        # Create a list to store user data dictionaries
        user_list = []

        for user in users:
            # Create a user data dictionary
            user_data = {
                'id': user.user_id,
                'public_id': user.public_id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
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
                    'payment_status': order.payment_status,
                    'order_reference_code': order.order_reference_code,
                    'packed': order.packed

                }
                user_data['orders'].append(order_data)

            # Extract user's storage units
            customer = user.customer
            if customer:
                storage_units = customer.orders
                for storage_unit in storage_units:
                    storage_unit_data = {
                        'id': storage_unit.storage_space.id,
                        'size': storage_unit.storage_space.size,
                        'price': storage_unit.storage_space.price,
                    }
                    user_data['storage_units'].append(storage_unit_data)

            user_list.append(user_data)

        # Return the user data list as JSON
        return jsonify({'users': user_list})

    except Exception as e:
        return jsonify({'error': str(e)})


# Route to get single user
@app.route('/users/<int:user_id>', methods=['GET'])
# @token_required
def get_single_user(user_id):
    try:
        # Query the user by user_id
        user = User.query.get(user_id)

        if user is not None:
            # Create a user data dictionary
            user_data = {
                'id': user.user_id,
                'public_id': user.public_id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
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
                    'payment_status': order.payment_status,
                    'order_reference_code': order.order_reference_code,
                    'packed': order.packed
                    # Add more fields as needed
                }
                user_data['orders'].append(order_data)

            # Extract user's storage units
            customer = user.customer
            if customer:
                storage_units = customer.orders
                for storage_unit in storage_units:
                    storage_unit_data = {
                        'id': storage_unit.storage_space.id,
                        'size': storage_unit.storage_space.size,
                        'price': storage_unit.storage_space.price,
                    }
                    user_data['storage_units'].append(storage_unit_data)

            # Return the user data as JSON
            return jsonify({'user': user_data})

        return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)})


# # Creating a user
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
            profile_picture=data.get('profile_picture'),
            address=data.get('address')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})
    except Exception as e:
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

        if 'password' in data:
            # Update password with a hashed version
            hashed_password = generate_password_hash(
                data['password'], method='pbkdf2:sha256')
            user.password = hashed_password

        db.session.commit()

        updated_user_data = {
            'user_id': user.user_id,
            'full_name': user.full_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
            'profile_picture': user.profile_picture,
            'address': user.address
        }

        return jsonify({'message': 'User updated successfully', 'user': updated_user_data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User update failed. Please try again later.'}), 500


# Creating orders
@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()

        print("Received Data:")
        print(data)

        # Validate the request data
        required_fields = ['user_id', 'delivery_date', 'total_price', 'number_of_items', 'invoice', 'payment_method',
                           'booking_date', 'booking_status', 'payment_status', 'pickup_date_scheduled', 'pickup_date_actual', 'order_reference_code']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Extract relevant data from the request
        user_id = data['user_id']
        delivery_date = datetime.fromisoformat(data['delivery_date'])
        total_price = data['total_price']
        number_of_items = data['number_of_items']
        invoice = data['invoice']
        payment_method = data['payment_method']
        booking_date = datetime.fromisoformat(data['booking_date'])
        booking_status = data['booking_status']
        payment_status = data['payment_status']
        pickup_date_scheduled = datetime.fromisoformat(
            data['pickup_date_scheduled'])
        pickup_date_actual = datetime.fromisoformat(data['pickup_date_actual'])
        order_reference_code = data['order_reference_code']

        print("Processed Data:")
        print("user_id:", user_id)
        print("delivery_date:", delivery_date)
        print("total_price:", total_price)
        print("number_of_items:", number_of_items)
        print("invoice:", invoice)
        print("payment_method:", payment_method)
        print("booking_date:", booking_date)
        print("booking_status:", booking_status)
        print("payment_status:", payment_status)
        print("pickup_date_scheduled:", pickup_date_scheduled)
        print("pickup_date_actual:", pickup_date_actual)
        print("order_reference_code:", order_reference_code)

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            print("User not found")
            return jsonify({'error': 'User not found'}), 404

        # Create a new order with the required parameters
        new_order = Order(
            user_id=user_id,
            order_date=datetime.now(),
            delivery_date=delivery_date,
            total_price=total_price,
            number_of_items=number_of_items,
            invoice=invoice,
            payment_method=payment_method,
            booking_date=booking_date,
            booking_status=booking_status,
            payment_status=payment_status,
            pickup_date_scheduled=pickup_date_scheduled,
            pickup_date_actual=pickup_date_actual,
            order_reference_code=order_reference_code,
            packed=True
        )

        # Add the order to the database
        db.session.add(new_order)
        db.session.commit()

        print("Order created successfully")
        return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        print("Order creation failed:", str(e))
        return jsonify({'error': 'Order creation failed. Please try again later.'}), 500


# Getting all orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    try:
        # Retrieve all orders from the database
        orders = Order.query.all()

        # Create a list to store the order data
        order_list = []

        # Iterate through the orders and convert them to a dictionary
        for order in orders:
            order_data = {
                'order_id': order.id,
                'user_id': order.user_id,
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
                'packed': order.packed
            }
            order_list.append(order_data)

        # Return the list of orders as JSON
        return jsonify({'orders': order_list})

    except Exception as e:
        print("Failed to retrieve orders:", str(e))
        return jsonify({'error': 'Failed to retrieve orders'}), 500

# Getting a single order


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    try:
        # Retrieve the order with the specified order_id from the database
        order = Order.query.get(order_id)

        if order is not None:
            # Convert the order data to a dictionary
            order_data = {
                'order_id': order.id,
                'user_id': order.user_id,
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
                'packed': order.packed
            }

            # Return the order data as JSON
            return jsonify(order_data)
        else:
            return jsonify({'error': 'Order not found'}), 404

    except Exception as e:
        print(f"Failed to retrieve order {order_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve order'}), 500

# Updating order


@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    # Retrieve the order from the database based on the order_id
    order = db.session.get(Order, order_id)  # Use Session.get()

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        if 'delivery_date' in data:
            # Parse the string date into a datetime object
            order.delivery_date = datetime.strptime(
                data['delivery_date'], '%Y-%m-%d %H:%M:%S')

        if 'order_reference_code' in data:
            order.order_reference_code = data['order_reference_code']

        if 'invoice' in data:
            order.invoice = data['invoice']

        if 'payment_method' in data:
            order.payment_method = data['payment_method']

        if 'number_of_items' in data:
            order.number_of_items = data['number_of_items']

        if 'booking_date' in data:
            # Parse the string date into a datetime object
            order.booking_date = datetime.strptime(
                data['booking_date'], '%Y-%m-%d %H:%M:%S')

        if 'booking_status' in data:
            order.booking_status = data['booking_status']

        if 'total_price' in data:
            order.total_price = data['total_price']

        if 'payment_status' in data:
            order.payment_status = data['payment_status']

        if 'pickup_date_scheduled' in data:
            # Parse the string date into a datetime object
            order.pickup_date_scheduled = datetime.strptime(
                data['pickup_date_scheduled'], '%Y-%m-%d %H:%M:%S')

        if 'pickup_date_actual' in data:
            # Parse the string date into a datetime object
            order.pickup_date_actual = datetime.strptime(
                data['pickup_date_actual'], '%Y-%m-%d %H:%M:%S')

        if 'packed' in data:
            order.packed = data['packed']

        # Add other order attributes that you want to update

        db.session.commit()

        updated_order_data = {
            'id': order.id,
            'user_id': order.user_id,
            'delivery_date': order.delivery_date.strftime('%Y-%m-%d %H:%M:%S'),
            'order_reference_code': order.order_reference_code,
            'invoice': order.invoice,
            'payment_method': order.payment_method,
            'number_of_items': order.number_of_items,
            'booking_date': order.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'booking_status': order.booking_status,
            'total_price': order.total_price,
            'payment_status': order.payment_status,
            'pickup_date_scheduled': order.pickup_date_scheduled.strftime('%Y-%m-%d %H:%M:%S'),
            'pickup_date_actual': order.pickup_date_actual.strftime('%Y-%m-%d %H:%M:%S'),
            'packed': order.packed,
        }

        print("Order updated successfully")

        return jsonify({'message': 'Order updated successfully', 'order': updated_order_data})
    except Exception as e:
        db.session.rollback()
        print(f"Order update failed. Error: {str(e)}")
        return jsonify({'error': 'Order update failed. Please try again later.'}), 500

# Deleting order


@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Retrieve the order from the database based on the order_id
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        # Delete the order from the database
        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Order deletion failed. Error: {str(e)}")
        return jsonify({'error': 'Order deletion failed. Please try again later.'}), 500


if __name__ == '__main__':
    app.run(debug=True)

