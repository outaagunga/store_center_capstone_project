from wtfforms import Form, IntegerField, validators


class StorageUnitForm(Form):
    price = IntegerField('Price', [
        validators.InputRequired(message="Price is required."),
        validators.NumberRange(min=0, message="Price must be a non-negative value.")
    ])