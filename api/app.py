# app.py
from flask import jsonify, request
from flask import jsonify
from flask import Flask, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'opuyoapuga'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storecenter.db'
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True)
