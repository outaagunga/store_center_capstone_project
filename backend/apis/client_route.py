from flask import Blueprint, request, jsonify
from models.dbconfig import db
from models.booking import Booking
from models.payment import Payment
from models.users import User



client_routes = Blueprint('clients', __name__)

DEFAULT_PAGE_SIZE = 10

@client_routes.route('/clients/<int:client_id>', methods=['GET'])
def get_client_details(client_id):
    # Retrieve a single client by ID
    client = User.query.get(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', DEFAULT_PAGE_SIZE, type=int)

    bookings = Booking.query.filter_by(client_id=client_id).paginate(page, page_size, False)

    response = {
        "user_details": client.to_dict(),
        "storage_units": [],
        "payments": [],
        "products": [],
        "review": []
    }

    for booking in bookings.items:
        response["storage_units"].append(booking.storage_unit.to_dict())  # Assuming you've defined to_dict method in your model or using to_dictrMixin
        for product in booking.products:
            response["products"].append(product.to_dict())

    payments = Payment.query.filter_by(client_id=client_id).all()
    for payment in payments:
        response["payments"].append(payment.to_dict())


    return jsonify(response)

@client_routes.route('/clients', methods=['GET'])
def get_all_clients():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', DEFAULT_PAGE_SIZE, type=int)

    clients = User.query.filter_by(user_type='client').paginate(page, page_size, False)
    results = []

    for client in clients.items:
        client_data = {
            "user_details": client.to_dict(),
            "storage_units": [],
            "payments": [],
            "products": [],
            "review": []
        }

        bookings = Booking.query.filter_by(client_id=client.user_id).all()
        for booking in bookings:
            client_data["storage_units"].append(booking.storage_unit.to_dict())
            for product in booking.products:
                client_data["products"].append(product.to_dict())

        payments = Payment.query.filter_by(client_id=client.user_id).all()
        for payment in payments:
            client_data["payments"].append(payment.to_dict())

        results.append(client_data)

    return jsonify({
        "clients": results,
        "total_pages": clients.pages
    })