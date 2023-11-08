from flask import Blueprint, jsonify, request, abort
from models.product import Product
from models.category import Category 
from models.users import User
from models.booking import Booking

from sqlalchemy.orm import joinedload

# Create the blueprint
product_routes = Blueprint('products', __name__)

# Number of records per page
PER_PAGE = 10

# Get all products with pagination
@product_routes.route('/products', methods=['GET'])
def get_all_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.options(
        joinedload(Product.category),
        joinedload(Product.booking).joinedload(Booking.client)
    ).paginate(page, PER_PAGE, error_out=False)  # error_out=False ensures it won't return 404 if beyond the page
    
    items = [{
        'name': product.name,
        'client_owner': f"{product.booking.client.first_name} {product.booking.client.last_name}",
        'category': product.category.name,
        'storage_unit': product.booking.storage_unit_name,  # Assuming you have this attribute in Booking
        'weight': product.weight,
        'quantity': product.quantity,
        'image_url': product.image_url,
        'description': product.description,
        'booking_id': product.booking_id
    } for product in products.items]

    return jsonify({
        'items': items,
        'next_page': products.next_num if products.has_next else None,
        'prev_page': products.prev_num if products.has_prev else None,
        'total_pages': products.pages
    })

# Get products by category with pagination
@product_routes.route('/products/by-category/<category_name>', methods=['GET'])
def get_products_by_category(category_name):
    page = request.args.get('page', 1, type=int)
    products = Product.query.options(
        joinedload(Product.category),
        joinedload(Product.booking).joinedload(Booking.client)
    ).filter(Category.name == category_name).paginate(page, PER_PAGE, error_out=False)

    items = [{
        'name': product.name,
        'client_owner': f"{product.booking.client.first_name} {product.booking.client.last_name}",
        'category': product.category.name,
        'storage_unit_size': product.booking.unit.size,  # Assuming you have this attribute in Booking
        'weight': product.weight,
        'quantity': product.quantity,
        'image_url': product.image_url,
        'description': product.description,
        'booking_id': product.booking_id
    } for product in products.items]

    return jsonify({
        'items': items,
        'next_page': products.next_num if products.has_next else None,
        'prev_page': products.prev_num if products.has_prev else None,
        'total_pages': products.pages
    })