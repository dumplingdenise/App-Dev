from wtforms import Form, StringField, SelectField, EmailField, PasswordField, \
    DecimalField, FloatField, validators, FileField, TextAreaField


class CreateProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = FloatField('Product Price', [validators.DataRequired()])
    stock = DecimalField('Product Stock', [validators.DataRequired()])
    description = TextAreaField('Product Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    agegroup = SelectField('Age Group', choices=[('0-2', '0-2'), ('3-6', '3-6'), ('7-12', '7-12'), ('12+', '12+')])
    file = FileField('Picture', [validators.DataRequired()])
    opfile = FileField('Picture')


class CustomerRegisterForm(Form):
    first_name = StringField('First name', [validators.DataRequired(), validators.Length(min=2, max=50)])
    last_name = StringField('Last name', [validators.DataRequired(), validators.Length(min=2, max=50)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    contact = StringField('Contact number', [validators.DataRequired(), validators.Length(min=8, max=8)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8)])
    cfmpw = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])


class StaffRegisterForm(Form):
    first_name = StringField('First name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    last_name = StringField('Last name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    role = SelectField('Role/Position', [validators.DataRequired()], choices=[('S', 'Staff'), ('A', 'Admin')],
                       default='S')
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=10)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    contact = StringField('Contact number', [validators.DataRequired(), validators.Length(min=8, max=8)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8)])
    cfmpw = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])


class CustomerLoginForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])


class StaffLoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=15)])
    password = PasswordField('Password', [validators.DataRequired()])


class CustomersupportForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=100), validators.DataRequired()])
    reasons = SelectField('Issues', [validators.DataRequired()],
                          choices=[('', 'Select'), ('order', 'Order issue'), ('ship', 'Shipment issue'),
                                   ('r/e', 'Refund/Exchange issue'), ('or', 'Others')], default='')
    email = StringField('Email', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.length(max=500), validators.DataRequired()])
    reply = TextAreaField('Reply to Customer', [validators.length(max=500), validators.DataRequired()])


class CreateOrderForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    contact_no = StringField('Contact No.', [validators.Length(min=1, max=8), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    notes = TextAreaField('Notes', [validators.length(max=200), validators.DataRequired()])
    cdname = StringField('Name on Card', [validators.Length(min=1, max=150), validators.DataRequired()])
    ccnum = StringField('Credit Card Number', [validators.Length(min=15, max=16), validators.DataRequired()])
    exp_mth = StringField('Expiry Month', [validators.Length(min=2, max=2), validators.DataRequired()])
    exp_yr = StringField('Expiry Year', [validators.Length(min=2, max=2), validators.DataRequired()])
    ccv = StringField('CCV', [validators.Length(min=3, max=4), validators.DataRequired()])
