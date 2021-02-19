from grocery_app.models import ItemCategory, GroceryStore, User
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from grocery_app import bcrypt


class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    # - title - StringField
    title = StringField('Store Name', validators=[DataRequired()])
    # - address - StringField
    address = StringField('Store Address', validators=[DataRequired()])
    # - submit button
    submit = SubmitField('Submit')


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # - name - StringField
    name = StringField('Item Name', validators=[DataRequired()])
    # - price - FloatField
    price = FloatField('Item Price', validators=[DataRequired()])
    # - category - SelectField (specify the 'choices' param)
    category = SelectField(
        'Item Category', choices=ItemCategory.choices())
    # - photo_url - StringField (use a URL validator)
    photo_url = StringField('Photo URL', validators=[DataRequired(), URL()])
    # - store - QuerySelectField (specify the `query_factory` param)
    store = QuerySelectField(
        'Store', query_factory=lambda: GroceryStore.query)
    # - submit button
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    """Form for creating a new user"""
    username = StringField('User Name',
                            validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField('User Name',
                            validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError(
                'No user found with that username.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError(
                'Password does not match.')