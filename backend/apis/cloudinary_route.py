from flask import request, jsonify, send_from_directory, redirect
import cloudinary
import cloudinary.uploader
from models import User, db  # or appropriate import path for your models
from sqlalchemy.exc import IntegrityError

# Configure cloudinary with app configurations
def configure_cloudinary(app):
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"]
    )

def cloudinary_routes(app):
    configure_cloudinary(app)

    @app.route('/upload', methods=['POST'])
    def upload_image():
        user_id = request.form.get('user_id')  # Getting user_id from the form
        context = request.form.get('context', 'default')
        file = request.files.get('image')

        if not file:
            return jsonify({"error": "No image provided"}), 400

        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        url = upload_result['secure_url']

        if context == 'profile':
            # Save this URL as a user's profile picture
            try:
                user = User.query.get(user_id)
                if user:
                    user.profile_image_url = url
                    db.session.add(user)
                    db.session.commit()
                else:
                    return jsonify({"error": "User not found"}), 404
            except IntegrityError:
                db.session.rollback()
                return jsonify({"error": "Error saving profile image URL"}), 500

        elif context == 'product':
            # Save this URL associated with a product
            # Similar logic for saving to a Product model (if one existed)
            pass

        elif context == 'storage':
            # Save this URL associated with a storage unit
            # Similar logic for saving to the StorageUnit model, if needed
            pass

        # ... handle other contexts

        return jsonify({"url": url, "context": context}), 200

    @app.route('/add_profile/<int:user_id>/<string:folder>', methods=['POST'])
    def add_profile(user_id, folder):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        upload_result = cloudinary.uploader.upload(file)
        url = upload_result['secure_url']

        user = User.query.get(user_id)
        if user:
            user.profile_image_url = url
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'message': 'Profile updated successfully',
                'url': url
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    @app.route('/uploads/profiles/<profile>', methods=["GET"])
    def get_profile(profile):
        user = User.query.filter_by(profile_image_url=profile).first()
        if user:
            return redirect(user.profile_image_url)  #  Redirect to the Cloudinary URL
        else:
            error_message = f"Image '{profile}' not found"
            return jsonify({"error": error_message}), 404