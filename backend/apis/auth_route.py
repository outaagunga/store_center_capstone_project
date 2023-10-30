from flask import Blueprint, request, jsonify, current_app, url_for
from models.users import User
from models.dbconfig import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from forms import RegistrationForm, LoginForm, ResetPasswordForm
from app import mail
import jwt
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

# Serializer for generating tokens
serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

# Configuration for JWT
SECRET_KEY = current_app.config['SECRET_KEY']
EXPIRATION = 3600  # Token validity in seconds



@auth.route('/signup', methods=['POST'])
def sign_up():
    form = RegistrationForm(request.form)
    
    if form.validate():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # Generate a token
        token = serializer.dumps(new_user.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

        # Save user to database with "verified" as False
        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        msg = Message('Verify your email', sender='your_email@example.com', recipients=[new_user.email])
        msg.body = f'Click here to verify your account: {url_for("auth.verify_email", token=token, _external=True)}'
        mail.send(msg)

        return jsonify({'message': 'User created, please check your email to verify your account!'}), 201

    return jsonify(form.errors), 400


@auth.route('/verify/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'message': 'User does not exist'}), 404

        user.verified = True
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Email verified successfully!'}), 200

    except:
        return jsonify({'message': 'The verification link is invalid or has expired'}), 400
    
    
@auth.route('/signin', methods=['POST'])
def sign_in():
    form = LoginForm(request.form)
    
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            return jsonify({'message': 'User does not exist'}), 404

        if not user.verified:
            return jsonify({'message': 'Please verify your email before logging in'}), 401

        if check_password_hash(user.password, form.password.data):
            token = jwt.encode({'user_id': user.user_id, 'exp': datetime.utcnow() + timedelta(seconds=EXPIRATION)}, SECRET_KEY)
            return jsonify({'token': token.decode('UTF-8')})

        return jsonify({'message': 'Invalid password'}), 401

    return jsonify(form.errors), 400



@auth.route('/request-reset', methods=['POST'])
def request_reset_password():
    form = ResetPasswordForm(request.form)
    
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            return jsonify({'message': 'Email not registered'}), 404

        # Generate a reset token
        token = serializer.dumps(user.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

        # Send password reset email
        msg = Message('Reset your password', sender='your_email@example.com', recipients=[user.email])
        msg.body = f'Click here to reset your password: {url_for("auth.reset_password", token=token, _external=True)}'
        mail.send(msg)

        return jsonify({'message': 'Please check your email for a password reset link'}), 200

    return jsonify(form.errors), 400


auth.route('/reset/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'message': 'Email not registered'}), 404

        form = ResetPasswordForm(request.form)
        if form.validate():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
            
            return jsonify({'message': 'Password reset successfully!'}), 200
        
        return jsonify(form.errors), 400

    except:
        return jsonify({'message': 'The reset link is invalid or has expired'}), 400