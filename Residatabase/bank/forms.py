from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class AddCustomerForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    CPR_number = IntegerField('CPR_number',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add')


class CustomerLoginForm(FlaskForm):
    id = IntegerField('CPR_number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EmployeeLoginForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class Search(FlaskForm):
    deposit = IntegerField('Maximum deposit in DKK')
    rent = IntegerField('Maximum monthly rent in DKK')
    kvm = IntegerField('Minimum square meters')
    dist = IntegerField('Maximum distance to UCPH in km')
    sort = SelectField('Sort by:',choices=[('rent','Rent'), ('size','Square meters'), ('distance','Distance')])
    Submit = SubmitField('Submit')

class TransferForm(FlaskForm):
    amount = IntegerField('amount', 
                        validators=[DataRequired()])
    #sourceAccountTest = SelectField('From Account test:', choices=dropdown_choices, validators=[DataRequired()])
    sourceAccount = SelectField('From Account:'  , choices=[], coerce = int, validators=[DataRequired()])
    targetAccount = SelectField('Target Account:', choices=[], coerce = int, validators=[DataRequired()])
    submit = SubmitField('Confirm')

class DepositForm(FlaskForm):
    amount = IntegerField('amount', 
                       validators=[DataRequired()])
    submit = SubmitField('Confirm')
    
class InvestForm(FlaskForm):
    submit = SubmitField('Confirm')