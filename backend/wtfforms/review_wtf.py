from wtforms import Form, IntegerField, validators

class ReviewForm(Form):
    rating = IntegerField('Rating', [
        validators.InputRequired(message="Rating is required."),
        validators.NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
    ])