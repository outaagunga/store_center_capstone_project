from flask_mail import Mail
from flask_bcrypt import Bcrypt


# Initializing Mail object without app context
mail = Mail()
bcrypt = Bcrypt()