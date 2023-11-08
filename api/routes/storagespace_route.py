
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


# Creating storage space
@app.route('/space', methods=['POST'])
def create_storage_space():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Define a list of required fields for a storage space
        required_fields = [
            'user_id',
            'name',
            'size',
            'capacity',
            'price_per_month',
            'address',
            'latitude',
            'longitude'
        ]

        # Check if all required fields are present
        missing_fields = [
            field for field in required_fields if field not in data
        ]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Parse and validate data
        try:
            user_id = int(data['user_id'])
            name = data['name']
            size = data['size']
            capacity = int(data['capacity'])
            price_per_month = float(data['price_per_month'])
            address = data['address']
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
            description = data.get('description', None)
            available = bool(data.get('available', True))
        except (ValueError, KeyError, TypeError):
            return jsonify({'error': 'Invalid data format in the request'}), 400

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Create a new storage space
        new_storage_space = StorageSpace(
            user_id=user_id,
            name=name,
            description=description,
            size=size,
            capacity=capacity,
            price_per_month=price_per_month,
            available=available,
            address=address,
            latitude=latitude,
            longitude=longitude
        )

        # Add the storage space to the database
        db.session.add(new_storage_space)
        db.session.commit()

        return make_response(jsonify({'message': 'Storage space created successfully', 'space_id': new_storage_space.id}), 201)

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Storage space creation failed. Please try again later.'}), 500

# Getting all stoge_spaces


@app.route('/space', methods=['GET'])
def get_all_storage_spaces():
    try:
        # Retrieve all storage spaces from the database
        storage_spaces = StorageSpace.query.all()

        # Prepare a list of storage space details
        storage_space_list = []

        for space in storage_spaces:
            # Simulate a scenario with more descriptive information
            space_details = {
                'id': space.id,
                'name': space.name,
                'description': space.description,
                'size': space.size,
                'capacity': space.capacity,
                'price_per_month': space.price_per_month,
                'available': space.available,
                'address': space.address,
                'location': {
                    'latitude': space.latitude,
                    'longitude': space.longitude
                }
            }

            # Include additional details based on availability
            if space.available:
                space_details['status'] = 'Available'
                space_details['availability_message'] = 'This storage space is ready for use.'
            else:
                space_details['status'] = 'Not Available'
                space_details['availability_message'] = 'This storage space is currently unavailable for booking.'

            storage_space_list.append(space_details)

        return jsonify(storage_space_list)

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve storage spaces'}), 500

# Getting single storage space


@app.route('/space/<int:space_id>', methods=['GET'])
def get_single_storage_space(space_id):
    try:
        # Retrieve a single storage space by its ID
        storage_space = StorageSpace.query.get(space_id)

        if not storage_space:
            return jsonify({'error': 'Storage space not found'}), 404

        # Prepare the details of the storage space
        space_details = {
            'id': storage_space.id,
            'name': storage_space.name,
            'description': storage_space.description,
            'size': storage_space.size,
            'capacity': storage_space.capacity,
            'price_per_month': storage_space.price_per_month,
            'available': storage_space.available,
            'address': storage_space.address,
            'location': {
                'latitude': storage_space.latitude,
                'longitude': storage_space.longitude
            }
        }

        # Include additional details based on availability
        if storage_space.available:
            space_details['status'] = 'Available'
            space_details['availability_message'] = 'This storage space is ready for use.'
        else:
            space_details['status'] = 'Not Available'
            space_details['availability_message'] = 'This storage space is currently unavailable for booking.'

        return jsonify(space_details)

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve the storage space'}), 500

# Deleting StorageSpace


@app.route('/space/<int:space_id>', methods=['DELETE'])
def delete_storage_space(space_id):
    try:
        storage_space = StorageSpace.query.get(space_id)

        if not storage_space:
            return jsonify({'error': 'Storage space not found'}), 404

        db.session.delete(storage_space)
        db.session.commit()

        return jsonify({'message': 'Storage space deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete the storage space. Please try again later.'}), 500


# Updating storage space


@app.route('/space/<int:space_id>', methods=['PUT'])
def update_storage_space(space_id):
    data = request.get_json()

    # Retrieve the storage space from the database based on the space_id
    storage_space = db.session.get(StorageSpace, space_id)

    if not storage_space:
        return jsonify({'error': 'Storage space not found'}), 404

    try:
        if 'name' in data:
            storage_space.name = data['name']

        if 'description' in data:
            storage_space.description = data['description']

        if 'size' in data:
            storage_space.size = data['size']

        if 'capacity' in data:
            storage_space.capacity = data['capacity']

        if 'price_per_month' in data:
            storage_space.price_per_month = data['price_per_month']

        if 'available' in data:
            storage_space.available = data['available']

        if 'address' in data:
            storage_space.address = data['address']

        if 'latitude' in data:
            storage_space.latitude = data['latitude']

        if 'longitude' in data:
            storage_space.longitude = data['longitude']

        # Add other storage space attributes that you want to update

        db.session.commit()

        updated_space_data = {
            'id': storage_space.id,
            'user_id': storage_space.user_id,
            'name': storage_space.name,
            'description': storage_space.description,
            'size': storage_space.size,
            'capacity': storage_space.capacity,
            'price_per_month': storage_space.price_per_month,
            'available': storage_space.available,
            'address': storage_space.address,
            'latitude': storage_space.latitude,
            'longitude': storage_space.longitude,
        }

        print("Storage space updated successfully")

        return jsonify({'message': 'Storage space updated successfully', 'space': updated_space_data})
    except Exception as e:
        db.session.rollback()
        print(f"Storage space update failed. Error: {str(e)}")
        return jsonify({'error': 'Storage space update failed. Please try again later.'}), 500
