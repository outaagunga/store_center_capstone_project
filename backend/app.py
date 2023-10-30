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
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import os





# creating flask app
app = Flask(__name__)



app.config.from_object(Config)
CORS(app)
bcrypt =Bcrypt(app)

# Initialize database
db.init_app(app)
Migrate(app, db)
mail = Mail(app)


if __name__ == '__main__':
    app.run()
