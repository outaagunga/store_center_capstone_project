# app.py
from flask import jsonify, request
from flask import request, jsonify, make_response, session
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.database import app
from routes.order_route import *
from models.routes import *
from models.authentication import *


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')
