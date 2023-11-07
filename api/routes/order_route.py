
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
from datetime import datetime
from models.database import db
from models.review import Review

# Creating order


@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        print("Received JSON data:", data)  # Print received data

        if not data:
            print("Invalid JSON data in the request")
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Define a list of required fields
        required_fields = [
            'user_id',
            'delivery_date',
            'total_price',
            'number_of_items',
            'booking_date',
            'booking_status',
            'payment_status',
            'pickup_date_scheduled',
            'pickup_date_actual',
            'order_reference_code',
        ]

        # Check if all required fields are present
        missing_fields = [
            field for field in required_fields if field not in data
        ]
        if missing_fields:
            print("Missing fields:", missing_fields)
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Parse and validate data
        try:
            user_id = int(data['user_id'])
            delivery_date = datetime.fromisoformat(data['delivery_date'])
            total_price = float(data['total_price'])
            number_of_items = int(data['number_of_items'])
            booking_date = datetime.fromisoformat(data['booking_date'])
            booking_status = data['booking_status']
            payment_status = data['payment_status']
            pickup_date_scheduled = datetime.fromisoformat(
                data['pickup_date_scheduled'])
            pickup_date_actual = datetime.fromisoformat(
                data['pickup_date_actual'])
            order_reference_code = data['order_reference_code']
        except (ValueError, KeyError, TypeError):
            print("Invalid data format in the request")
            return jsonify({'error': 'Invalid data format in the request'}), 400

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            print("User not found")
            return jsonify({'error': 'User not found'}), 404

        # Check for duplicate order reference code
        if Order.query.filter_by(order_reference_code=order_reference_code).first():
            print("Order with the same reference code already exists")
            return jsonify({'error': 'Order with the same reference code already exists'}), 400

        # Create a new order
        new_order = Order(
            user_id=user_id,
            delivery_date=delivery_date,
            total_price=total_price,
            number_of_items=number_of_items,
            booking_date=booking_date,
            booking_status=booking_status,
            payment_status=payment_status,
            pickup_date_scheduled=pickup_date_scheduled,
            pickup_date_actual=pickup_date_actual,
            order_reference_code=order_reference_code,
            packed=True,
            pickup_status=False,  # Change to a default value or set it based on your requirements
            pickup_address='',  # Change to a default value or set it based on your requirements
        )

        # Add the order to the database
        db.session.add(new_order)
        db.session.commit()

        print("Order created successfully")
        return make_response(jsonify({'message': 'Order created successfully', 'order_id': new_order.id}),
                             201)
    except Exception as e:
        db.session.rollback()
        print("Order creation failed. Exception:", str(e))
        return jsonify({'error': 'Order creation failed. Please try again later.'}), 500


# Route for updating a specific order

@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    # Retrieve the order from the database based on the order_id
    order = Order.query.get(order_id)  # Use Query.get() to get the order

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


# Getting all orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    try:
        # Retrieve all orders from the database
        orders = Order.query.all()

        # Create a list to store the details of each order
        orders_details = []
        for order in orders:
            order_detail = {
                'order_id': order.id,
                'user_id': order.user_id,
                'delivery_date': order.delivery_date.isoformat(),
                'total_price': order.total_price,
                'number_of_items': order.number_of_items,
                'booking_date': order.booking_date.isoformat(),
                'booking_status': order.booking_status,
                'payment_status': order.payment_status,
                'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                'pickup_date_actual': order.pickup_date_actual.isoformat(),
                'order_reference_code': order.order_reference_code,
                'packed': order.packed,
                'pickup_status': order.pickup_status,
                'pickup_address': order.pickup_address,
            }
            orders_details.append(order_detail)

        return jsonify({'orders': orders_details})

    except Exception as e:
        print("Error while fetching orders:", str(e))
        return jsonify({'error': 'Failed to retrieve orders'}), 500

# Getting a specific order


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        # Retrieve the order from the database by its ID
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Format the order details
        order_detail = {
            'order_id': order.id,
            'user_id': order.user_id,
            'delivery_date': order.delivery_date.isoformat(),
            'total_price': order.total_price,
            'number_of_items': order.number_of_items,
            'booking_date': order.booking_date.isoformat(),
            'booking_status': order.booking_status,
            'payment_status': order.payment_status,
            'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
            'pickup_date_actual': order.pickup_date_actual.isoformat(),
            'order_reference_code': order.order_reference_code,
            'packed': order.packed,
            'pickup_status': order.pickup_status,
            'pickup_address': order.pickup_address,
        }

        return jsonify({'order': order_detail})

    except Exception as e:
        print("Error while fetching order:", str(e))
        return jsonify({'error': 'Failed to retrieve the order'}), 500
