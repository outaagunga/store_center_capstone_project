from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate


app = Flask(__name__)


app.config['SECRET_KEY'] = 'opuyoapuga',
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:975129216@localhost/storecenter'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy()
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
