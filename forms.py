from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=200, message="Username must be between 4 and 200 characters")])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=20, message="Password must be between 4 and 20 characters")])

    email = StringField("Email", validators=[InputRequired(),
                                            Email(message="Please enter a valid Email address")])

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=100)])

    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=100)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=200, message="Username must be between 4 and 200 characters")])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=20, message="Password must be between 4 and 20 characters")])

class TransferForm(FlaskForm):
    email = StringField("Recipient Email", validators=[InputRequired(),
                                            Email(message="Please enter a valid Email address")])

    amount = FloatField("Amount", validators=[InputRequired()])    

class ProfileForm(FlaskForm):
    address = StringField("Address", validators=[InputRequired()])
    company = StringField("Company", validators=[InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
