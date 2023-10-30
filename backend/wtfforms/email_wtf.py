from wtforms import Form, StringField, validators

class UserForm(Form):
    email = StringField('Email', [
        validators.InputRequired(message="Email is required."),
        validators.Email(message="Invalid email format.")
    ])