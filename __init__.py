import Users.Customer
import Users.Staff
import Users.User
import os
import shelve
import classes.Order

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

import classes.customersupport as customer_support
import classes.toy as Toy
from Forms import CustomersupportForm, CreateProductForm, CustomerRegisterForm, CustomerLoginForm, StaffLoginForm, \
    StaffRegisterForm, CreateOrderForm

# install flask, flask-wtf, wtforms

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/adminHome')
def adminhome():
    customers_dict = {}
    try:
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()
    except:
        print('Error in retrieving Customers from customer.db')

    products_dict = {}
    try:
        db = shelve.open('products.db', 'r')
        products_dict = db['Products']
        db.close()
    except:
        print('Error in retrieving products from products.db')

    customer_support_dict = {}
    try:
        db = shelve.open('customersupport.db', 'r')
        customer_support_dict = db['Customers Support']
        db.close()
    except:
        print('Error')

    product_count = len(products_dict)
    customer_count = len(customers_dict)
    support_count = len(customer_support_dict)

    return render_template('adminhome.html', customer_count=customer_count, product_count=product_count,
                           support_count=support_count)


app.config['SECRET_KEY'] = 'secret'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/createproduct', methods=['GET', 'POST'])
def createproduct():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST':
        products_dict = {}
        db = shelve.open('products.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving products from product.db.")
        toy = Toy.Toy(create_product_form.name.data, "{:.2f}".format(create_product_form.price.data),
                      int(create_product_form.stock.data), create_product_form.description.data,
                      create_product_form.agegroup.data)
        toy.set_product_id(str(len(products_dict) + 1))

        file = request.files['file']
        filename = secure_filename(file.filename)
        imagedir = 'static/products/' + toy.get_product_id()
        try:
            os.makedirs(imagedir)
        except:
            pass
        file.save(os.path.join(imagedir, filename))
        toy.set_imagepath(imagedir + '/' + filename)

        products_dict[toy.get_product_id()] = toy
        db['Products'] = products_dict
        db.close()
        return redirect(url_for('retrieve_products'))
    return render_template('createProduct.html', form=create_product_form)


@app.route('/retrieveProducts')
def retrieve_products():
    try:
        products_dict = {}
        db = shelve.open('products.db', 'r')
        products_dict = db['Products']
        db.close()

        products_list = []
        for key in products_dict:
            product = products_dict.get(key)
            products_list.append(product)

        return render_template('retrieveProduct.html', count=len(products_list), products_list=products_list)
    except:
        return render_template('retrieveProduct.html', count=0)


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('products.db', 'w')
    products_dict = db['Products']

    product = products_dict.get(str(id))
    products_dict.pop(str(id))

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_products'))


@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST':
        products_dict = {}
        db = shelve.open('products.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(str(id))
        if update_product_form.opfile.data != '':
            print('changing pic')
            file = request.files['opfile']
            filename = secure_filename(file.filename)
            imagedir = 'static/products/' + product.get_product_id()
            try:
                os.makedirs(imagedir)
            except:
                pass
            file.save(os.path.join(imagedir, filename))
            product.set_imagepath(imagedir + '/' + filename)

        product.set_name(update_product_form.name.data)
        product.set_price("{:.2f}".format(update_product_form.price.data))
        product.set_stock(update_product_form.stock.data)
        product.set_description(update_product_form.description.data)

        db['Products'] = products_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    else:
        products_dict = {}
        db = shelve.open('products.db', 'r')
        products_dict = db['Products']
        db.close()
        product = products_dict.get(str(id))
        update_product_form.name.data = product.get_name()
        update_product_form.price.data = product.get_price()
        update_product_form.agegroup.data = product.get_agegroup()
        update_product_form.stock.data = product.get_stock()
        update_product_form.description.data = product.get_description()

        return render_template('updateProduct.html', form=update_product_form)


@app.route('/productPage', methods=['GET', 'POST'])
def productpage():
    try:
        products_dict = {}
        db = shelve.open('products.db', 'r')
        products_dict = db['Products']
        db.close()

        products_list = []
        for key in products_dict:
            product = products_dict.get(key)
            products_list.append(product)

        return render_template('productPage.html', products_list=products_list)
    except:
        return render_template('productPage.html')


@app.route('/productPage/<int:id>/')
def productdetail(id):
    products_dict = {}
    db = shelve.open('products.db', 'r')
    products_dict = db['Products']
    db.close()
    product = products_dict.get(str(id))

    return render_template('productDetail.html', product=product)


@app.route('/shoppingCart')
def cart():
    global totalprice
    global total
    products_dict = {}
    db = shelve.open('products.db', 'r')
    products_dict = db['Products']
    db.close()
    productList = []
    cart = []
    total = 0
    try:
        for x in session['cart']:
            print(x)
            productId = x[0]
            product = products_dict.get(productId)
            print(product)
            productList.append(product)
        for x in range(len(productList)):
            avg = (float(productList[x].get_price()) * session['cart'][x][1])
            avgg = f'%.2f' % avg
            cartitem = [productList[x], session['cart'][x][1], avgg]
            cart.append(cartitem)
            total += avg
            totalprice = f'%.2f' % total

        return render_template('shoppingCart.html', cart=cart, count=len(productList), totalprice=totalprice)
    except:
        return render_template('shoppingCart.html', count=0)


@app.route('/clearcart')
def clearcart():
    global cartlist
    global total
    global totalprice
    cartlist = []
    session['cart'] = cartlist
    total = 0
    totalprice = 0
    return redirect(url_for('cart'))


@app.route('/addcart', methods=['POST'])
def AddCart():
    global cartlist
    if 'cartlist' not in globals():
        cartlist = []
    product_id = request.form.get('productId')
    quantity = int(request.form.get('quantity'))

    for x in cartlist:
        if x[0] == product_id:
            oldquantity = x[1]
            cartlist.remove(x)
            cartitem = [product_id, (oldquantity + quantity)]
            cartlist.append(cartitem)
            session['cart'] = cartlist
            return redirect(url_for('cart'))

    cartitem = [product_id, quantity]
    cartlist.append(cartitem)
    session['cart'] = cartlist
    return redirect(url_for('cart'))


@app.route('/retrieveOrders')
def retrieve_orders():
    orders_dict = {}
    db = shelve.open('orders.db', 'r')
    orders_dict = db['Orders']
    db.close()

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)

    return render_template('retrieveOrder.html', count=len(orders_list), orders_list=orders_list)


@app.route('/updateOrder/<int:id>/', methods=['GET', 'POST'])
def update_order(id):
    update_order_form = CreateOrderForm(request.form)
    if request.method == 'POST' and update_order_form.validate():
        orders_dict = {}
        db = shelve.open('orders.db', 'w')
        orders_dict = db['Orders']

        order = orders_dict.get(id)
        order.set_first_name(update_order_form.first_name.data)
        order.set_last_name(update_order_form.last_name.data)
        order.set_contact_no(update_order_form.contact_no.data)
        order.set_email(update_order_form.email.data)
        order.set_address(update_order_form.address.data)
        order.set_notes(update_order_form.notes.data)

        db['Orders'] = orders_dict
        db.close()

        return redirect(url_for('home'))
    else:
        orders_dict = {}
        db = shelve.open('orders.db', 'r')
        orders_dict = db['Orders']
        db.close()

        order = orders_dict.get(id)
        update_order_form.first_name.data = order.get_first_name()
        update_order_form.last_name.data = order.get_last_name()
        update_order_form.contact_no.data = order.get_contact_no()
        update_order_form.email.data = order.get_email()
        update_order_form.address.data = order.get_address()
        update_order_form.notes.data = order.get_notes()

        return render_template('updateOrder.html', form=update_order_form)


@app.route('/deleteOrder/<int:id>', methods=['POST'])
def delete_order(id):
    orders_dict = {}
    db = shelve.open('orders.db', 'w')
    orders_dict = db['Orders']

    orders_dict.pop(id)

    db['Orders'] = orders_dict
    db.close()

    return redirect(url_for('retrieve_orders'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    global cartlist
    global total
    global totalprice
    create_order_form = CreateOrderForm(request.form)
    if request.method == 'POST' and create_order_form.validate():
        orders_dict = {}
        db = shelve.open('orders.db', 'c')

        try:
            orders_dict = db['Orders']
        except:
            print("Error in retrieving orders from orders.db")

        order = classes.Order.Order('admin', create_order_form.first_name.data, create_order_form.last_name.data,
                                    create_order_form.contact_no.data, create_order_form.email.data,
                                    create_order_form.address.data, create_order_form.notes.data,
                                    create_order_form.cdname.data, create_order_form.ccnum.data,
                                    create_order_form.exp_mth.data, create_order_form.exp_yr.data,
                                    create_order_form.ccv.data)

        order.set_order_id((len(orders_dict) + 1))
        orders_dict[order.get_order_id()] = order
        db['Orders'] = orders_dict

        db.close()

        cartlist = []
        session['cart'] = cartlist
        total = 0
        totalprice = 0
        return redirect(url_for('confirm'))
    else:
        id = session['user_id']
        customers_dict = {}
        try:
            db = shelve.open('customer.db', 'r')
            customers_dict = db['Customers']
            db.close()
        except:
            print('Error in retrieving customers in customer.db')

        customer = customers_dict.get(id)
        create_order_form.first_name.data = customer.get_first_name()
        create_order_form.last_name.data = customer.get_last_name()
        create_order_form.contact_no.data = customer.get_contact()
        create_order_form.email.data = customer.get_email()

        return render_template('checkout.html', form=create_order_form)


@app.route('/confirm')
def confirm():
    return render_template('orderConfirmation.html')


@app.route('/customerRegister', methods=['GET', 'POST'])
def customer_Register():
    form = CustomerRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            customers_dict = db['Customers']
        except:
            print('Error in retrieving Customers from customer.db')

        customer = Users.Customer.Customer(form.first_name.data, form.last_name.data,
                                           form.email.data, form.contact.data, form.password.data,
                                           form.cfmpw.data)
        customers_dict[customer.get_Customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()
        session['user_id'] = customer.get_Customer_id()
        session['user_created'] = customer.get_first_name() + ' ' + customer.get_last_name()
        session['user_email'] = customer.get_email()
        session['user_contact'] = customer.get_contact()
        return redirect(url_for('customerhome'))
    return render_template('customerRegister.html', form=form, active='reg_login')


@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    try:
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()
    except:
        print('Error in retrieving Customers from customer.db')

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


@app.route('/login')
def login():
    return render_template('login.html', active='reg_login')


@app.route('/customerLogin', methods=['GET', 'POST'])
def customer_Login():
    form = CustomerLoginForm(request.form)
    if request.method == "POST" and form.validate():
        customers_dict = {}
        try:
            db = shelve.open('customer.db', 'r')
            customers_dict = db['Customers']
            db.close()
        except:
            print('Error in retrieving customers in customer.db')

        customers_list = []
        for key in customers_dict:
            customer = customers_dict.get(key)
            customers_list.append(customer)

        email_list = []
        for key in customers_dict:
            customer = customers_dict.get(key)
            emailadd = customer.get_email()
            email_list.append(emailadd)

        password_list = []
        for key in customers_dict:
            customer = customers_dict.get(key)
            pw = customer.get_password()
            password_list.append(pw)

        EMAILCHECK = False
        PASSWORDCHECK = False
        for customer in customers_list:
            if form.email.data == customer.get_email() and form.password.data == customer.get_password():
                EMAILCHECK = True
                PASSWORDCHECK = True
                session['user_created'] = customer.get_first_name() + ' ' + customer.get_last_name()
                session['user_id'] = customer.get_Customer_id()

        if EMAILCHECK == True and PASSWORDCHECK == True:
            return redirect(url_for('customerhome'))
        else:
            print('Email or Password does not match !')
            return render_template('customerLogin.html', form=form, active='reg_login', wrong='wrong')
    return render_template('customerLogin.html', form=form, active='reg_login')


@app.route('/staffLogin', methods=['GET', 'POST'])
def staff_Login():
    form = StaffLoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = request.form['username']
        session['username'] = username
        if username == 'Admin123' and form.password.data == 'Admin1234':
            return redirect(url_for('adminhome'))
        else:
            staff_dict = {}
            db = shelve.open('staff.db', 'r')
            try:
                staff_dict = db['Staff']
                db.close()
            except:
                print('Error in retrieving Users in staff.db')

            staff_list = []
            for key in staff_dict:
                staff = staff_dict.get(key)
                staff_list.append(staff)

            username_list = []
            for key in staff_dict:
                staff = staff_dict.get(key)
                username = staff.get_username()
                username_list.append(username)

            password_list = []
            for key in staff_dict:
                staff = staff_dict.get(key)
                pw = staff.get_password()
                password_list.append(pw)

            USERNAMECHECK = False
            PASSWORDCHECK = False
            for staff in staff_list:
                if username == staff.get_username() and form.password.data == staff.get_password():
                    USERNAMECHECK = True
                    PASSWORDCHECK = True

            if USERNAMECHECK == True and PASSWORDCHECK == True:
                return redirect(url_for('adminhome'))
            else:
                return render_template('staffLogin.html', wrong='wrong', form=form)

    return render_template('staffLogin.html', form=form, active='reg_login')


@app.route('/staffManagement')
def staff_Management():
    staff_dict = {}
    db = shelve.open('staff.db', 'c')
    try:
        staff_dict = db['Staff']
        db.close()
    except:
        print('Error in retrieving Users in staff.db')

    staff_list = []
    for key in staff_dict:
        staff = staff_dict.get(key)
        staff_list.append(staff)

    return render_template('staffManagement.html', count=len(staff_list), staff_list=staff_list)


@app.route('/staffRegister', methods=['GET', 'POST'])
def staff_Register():
    form = StaffRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')

        try:
            staff_dict = db['Staff']
        except:
            print('Error in retrieving Staffs from staff.db')

        staff = Users.Staff.Staff(form.first_name.data, form.last_name.data, form.role.data, form.username.data,
                                  form.email.data, form.contact.data, form.password.data,
                                  form.cfmpw.data)
        staff_dict[staff.get_Staff_id()] = staff
        db['Staff'] = staff_dict

        db.close()
        return redirect(url_for('staff_Management'))
    return render_template('staffRegister.html', form=form)


@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    form = StaffRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        staff = staff_dict.get(id)
        staff.set_first_name(form.first_name.data)
        staff.set_last_name(form.last_name.data)
        staff.set_email(form.email.data)
        staff.set_contact(form.contact.data)
        staff.set_password(form.password.data)
        staff.set_cfmpw(form.cfmpw.data)

        db['Staff'] = staff_dict
        db.close()

        return redirect(url_for('staff_Management'))
    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        staff = staff_dict.get(id)
        form.first_name.data = staff.get_first_name()
        form.last_name.data = staff.get_last_name()
        form.role.data = staff.get_role()
        form.username.data = staff.get_username()
        form.email.data = staff.get_email()
        form.contact.data = staff.get_contact()
        form.password.data = staff.get_password()
        form.cfmpw.data = staff.get_cfmpw()

        return render_template('updateStaff.html', form=form)


@app.route('/deleteStaff/<int:id>/', methods=['GET', 'POST'])
def delete_staff(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']

    staff_dict.pop(id)

    db['Staff'] = staff_dict
    db.close()

    return redirect(url_for('staff_Management'))


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    form = CustomerRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(form.first_name.data)
        customer.set_last_name(form.last_name.data)
        customer.set_email(form.email.data)
        customer.set_contact(form.contact.data)
        customer.set_password(form.password.data)
        customer.set_cfmpw(form.cfmpw.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        form.first_name.data = customer.get_first_name()
        form.last_name.data = customer.get_last_name()
        form.email.data = customer.get_email()
        form.contact.data = customer.get_contact()
        form.password.data = customer.get_password()
        form.cfmpw.data = customer.get_cfmpw()

        return render_template('updateCustomer.html', form=form)


@app.route('/deleteCustomer/<int:id>/', methods=['GET', 'POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']

    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))


@app.route('/customerHome')
def customerhome():
    return render_template('customerHome.html', active='customerhome')


@app.route('/myAccount')
def myAccount():
    id = session['user_id']
    customers_dict = {}
    try:
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()
    except:
        print('Error in retrieving customers in customer.db')

    customer = customers_dict.get(id)

    return render_template('myAccount.html', customer=customer)


@app.route('/customerEdit', methods=['GET', 'POST'])
def customerEdit():
    customerid = session['user_id']
    form = CustomerRegisterForm(request.form)
    if request.method == "POST":
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(customerid)
        customer.set_first_name(form.first_name.data)
        customer.set_last_name(form.last_name.data)
        customer.set_email(form.email.data)
        customer.set_contact(form.contact.data)
        customer.set_password(form.password.data)
        customer.set_cfmpw(form.cfmpw.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('customerhome'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()
        customer = customers_dict.get(customerid)

        form.first_name.data = customer.get_first_name()
        form.last_name.data = customer.get_last_name()
        form.email.data = customer.get_email()
        form.contact.data = customer.get_contact()
        form.password.data = customer.get_password()
        form.cfmpw.data = customer.get_cfmpw()

        return render_template('customerEdit.html', form=form)


@app.route('/customersupport', methods=['GET', 'POST'])
def customersupport():
    customer_support_form = CustomersupportForm(request.form)
    if request.method == 'POST':
        customer_support_dict = {}
        db = shelve.open('customersupport.db', 'c')

        try:
            customer_support_dict = db['Customers Support']
        except:
            print("Error in retrieving Customer feedback from customersupport.db.")

        customer = customer_support.customer_support(customer_support_form.name.data,
                                                     customer_support_form.reasons.data,
                                                     customer_support_form.email.data,
                                                     customer_support_form.description.data)
        customer.set_customer_support_id((len(customer_support_dict) + 1))
        customer_support_dict[customer.get_customer_support_id()] = customer
        db['Customers Support'] = customer_support_dict

        db.close()

        return redirect(url_for('customerhome'))
    return render_template('customersupport.html', form=customer_support_form)


@app.route('/retrievecustomerfeedback')
def retrieve_customer_feedback():
    customer_support_dict = {}
    db = shelve.open('customersupport.db', 'r')
    customer_support_dict = db['Customers Support']
    db.close()

    customer_support_list = []
    for key in customer_support_dict:
        customer = customer_support_dict.get(key)
        customer_support_list.append(customer)

    return render_template('retrievecustomerfeedback.html', count=len(customer_support_list),
                           customersupport_list=customer_support_list)


@app.route('/deletecustomersupport/<int:id>', methods=['POST'])
def delete_customersupport(id):
    customer_support_dict = {}
    db = shelve.open('customersupport.db', 'w')
    customer_support_dict = db['Customers Support']

    customer_support_dict.pop(id)

    db['Customers Support'] = customer_support_dict
    db.close()

    return redirect(url_for('retrieve_customer_feedback'))


@app.route('/updatecustomerfeedback/<int:id>/', methods=['GET', 'POST'])
def update_customer_support(id):
    update_customer_support_form = CustomersupportForm(request.form)
    if request.method == 'POST' and update_customer_support_form.validate():
        customer_support_dict = {}
        db = shelve.open('customersupport.db', 'w')
        customer_support_dict = db['Customers Support']

        customer = customer_support_dict.get(id)
        customer.set_name(update_customer_support_form.name.data)
        customer.set_reasons(update_customer_support_form.reasons.data)
        customer.set_email(update_customer_support_form.email.data)
        customer.set_description(update_customer_support_form.description.data)
        customer.set_reply(update_customer_support_form.reply.data)

        db['Customers Support'] = customer_support_dict
        db.close()

        return redirect(url_for('retrieve_customer_feedback'))
    else:
        db = shelve.open('customersupport.db', 'r')
        customer_support_dict = db['Customers Support']
        db.close()

        customer = customer_support_dict.get(id)
        update_customer_support_form.name.data = customer.get_name()
        update_customer_support_form.reasons.data = customer.get_reasons()
        update_customer_support_form.email.data = customer.get_email()
        update_customer_support_form.description.data = customer.get_description()
        update_customer_support_form.reply.data = customer.get_reply()

        return render_template('updatecustomerfeedback.html', form=update_customer_support_form)


@app.route('/logout')
def logout():
    global cartlist
    cartlist = []
    session['cart'] = []
    for key in list(session.keys()):
        session.pop(key)
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
