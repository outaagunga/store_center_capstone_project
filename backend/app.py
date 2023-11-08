from flask import Flask 
from models.users import User
from models.booking import Booking
from models.pickupDelivery import PickUpDelivery
from models.review import Review
from models.dbconfig import db
from models.storageUnit import StorageUnit
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from extensions import mail, bcrypt

import os


def create_app(config_class=Config):
    # creating flask app
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    
    # Initialize flask extensions
    # bcrypt =Bcrypt(app)
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)
    
     # Register blueprints within the application context
    with app.app_context():
        from apis.auth_route import auth_routes
        from apis.user_route import user_routes
        from apis.booking_route import booking_routes
        from apis.review_route import review_routes
        from apis.pickupdelivery_route import delivery_routes
        from apis.client_route import client_routes
        from apis.cloudinary_route import cloudinary_routes,configure_cloudinary_routes
        from apis.products_route import product_routes
        
        # Attach Cloudinary routes
        configure_cloudinary_routes(app)


        # Register blueprints
        app.register_blueprint(auth_routes, url_prefix='/api/auth')
        app.register_blueprint(user_routes, url_prefix='/api/users')
        app.register_blueprint(booking_routes, url_prefix='/api/bookings')
        app.register_blueprint(review_routes, url_prefix='/api/reviews')
        # app.register_blueprint(service_routes, url_prefix='/api/services')
        app.register_blueprint(cloudinary_routes, url_prefix='/api/cloudinary')
        app.register_blueprint(delivery_routes, url_prefix='/api/pickupDelivery')
        app.register_blueprint(client_routes, url_prefix='/api/clients')
        app.register_blueprint(product_routes, url_prefix='/api/products')
        # app.register_blueprint(storageunit_routes, url_prefix='/api/storage_units')
        # app.register_blueprint(category_routes, url_prefix='/api/categories')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
