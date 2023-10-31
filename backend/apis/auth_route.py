from flask import Blueprint, request, jsonify, current_app, url_for
from models.users import User
from models.dbconfig import db
from config import redis_client 
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from forms import RegistrationForm, LoginForm, ResetPasswordForm
from app import mail
import jwt
from random import randint
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
            # Generate a random 6-digit code for 2FA
            code = randint(100000, 999999)
            # Store the code in Redis with the user's ID as the key and 
            # set an expiration time
            redis_client.setex(f"2FA-{user.id}", EXPIRATION, code)

            # Store the code temporarily with the user's ID and timestamp (pseudo-code)
            # store_2fa_code(user.id, code, timestamp=datetime.utcnow())

            # Send 2FA code via email
            msg = Message('Your 2FA Code', sender='your_email@example.com', recipients=[user.email])
            msg.body = f'Your verification code is: {code}'
            mail.send(msg)

            return jsonify({'message': '2FA code sent to email. Please verify to proceed.'}), 202

        return jsonify({'message': 'Invalid password'}), 401

    return jsonify(form.errors), 400


@auth.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    user_id = request.form.get('user_id')
    code = request.form.get('code')

    # Fetch the stored code from Redis
    stored_code = redis_client.get(f"2FA-{user_id}")

    # Validate that the code matches and is not expired
    if stored_code and code == stored_code.decode():
        # Remove the stored 2FA code from Redis since it's used now
        redis_client.delete(f"2FA-{user_id}")

        token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(seconds=EXPIRATION)}, SECRET_KEY)
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'message': 'Invalid or expired 2FA code'}), 401



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