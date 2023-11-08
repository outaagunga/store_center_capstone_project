from flask import request, jsonify, Blueprint
from flask_mail import Message
from extensions import mail
from models.pickupDelivery import PickUpDelivery
from models.users import User



delivery_routes = Blueprint('pickupDelivery', __name__)
    
    

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to])
    msg.body = template
    mail.send(msg)

@delivery_routes.route('/pickup/schedule', methods=['POST'])
def schedule_pickup():
    client_id = request.json.get('client_id')
    date = request.json.get('date')
    address = request.json.get('address')

    pickup = PickUpDelivery.create_pickup_or_delivery(client_id, 'pickup', date, address)
    if pickup:
        client = User.query.get(client_id)
        send_email(client.email, "Pickup Scheduled", f"Dear {client.first_name},\n\nYour pickup has been scheduled for {date} at {address}.")
        return jsonify(pickup.to_dict()), 201
    return jsonify({'error': 'Failed to schedule pickup'}), 400

@delivery_routes.route('/delivery/schedule', methods=['POST'])
def schedule_delivery():
    client_id = request.json.get('client_id')
    date = request.json.get('date')
    address = request.json.get('address')

    delivery = PickUpDelivery.create_pickup_or_delivery(client_id, 'delivery', date, address)
    if delivery:
        client = User.query.get(client_id)
        send_email(client.email, "Delivery Scheduled", f"Dear {client.first_name},\n\nYour delivery has been scheduled for {date} at {address}.")
        return jsonify(delivery.to_dict()), 201
    return jsonify({'error': 'Failed to schedule delivery'}), 400

@delivery_routes.route('/status/<int:service_id>', methods=['PUT'])
def update_status(service_id):
    new_status = request.json.get('status')
    
    service = PickUpDelivery.update_service_status(service_id, new_status)
    if service:
        client = User.query.get(service.client_id)
        send_email(client.email, "Service Status Updated", f"Dear {client.first_name},\n\nThe status of your service (ID: {service_id}) has been updated to {new_status}.")
        return jsonify(service.to_dict()), 200
    return jsonify({'error': 'Failed to update status'}), 400

@delivery_routes.route('/services', methods=['GET'])
def list_client_services():
    client_id = request.args.get('client_id')
    services = PickUpDelivery.get_services_by_client(client_id)
    return jsonify([service.to_dict() for service in services]), 200