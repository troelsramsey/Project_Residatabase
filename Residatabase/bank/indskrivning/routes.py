from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import CustomerLoginForm, EmployeeLoginForm, Search
from flask_login import login_user, current_user, logout_user, login_required
from bank.models import Customers, select_Customers, select_Employees, search_apt

Indskrivning = Blueprint('Indskrivning', __name__)

posts = [{}]


@Indskrivning.route("/", methods=['GET', 'POST'])
def home2():
    form = Search()
    if form.deposit.data == None:
        form.deposit.data = 100000
    if form.rent.data == None:
        form.rent.data = 15000
    if form.kvm.data == None:
        form.kvm.data = 0
    if form.dist.data == None:
        form.dist.data = 500
    if form.validate_on_submit():
        apt = search_apt(form.deposit.data, form.rent.data, form.dist.data, form.kvm.data, form.sort.data)
        print("\nhej: ", apt, "\n")
        if apt == None:
            return render_template('home2.html', posts=posts, form=form)
        return render_template('enroll.html', title='Login', apt=apt, form=form)
    return render_template('home2.html', posts=posts, form=form)


@Indskrivning.route("/about")
def about():
    return render_template('about.html', title='About')

@Indskrivning.route("/result")
def results():
    return render_template('enroll.html', title='result')

@Indskrivning.route("/Indskrivning", methods=['GET', 'POST'])
def search():
    form = Search()
    print(form)
    print(form.deposit.data, form.rent.data, form.dist.data, form.kvm.data)
    # if form.deposit.data == None:
        
    #  form.rent.data == None or form.dist.data == None or form.kvm.data == None
    apt = search_apt(10000, 6000, 50, 65)
    print(apt)
        # if user != None and bcrypt.check_password_hash(user[2], form.password.data):
        #     login_user(user, remember=form.remember.data)
        #     flash('Login successful.','success')
        #     next_page = request.args.get('next')
        #     return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        # else:
        #     flash('Login Unsuccessful. Please check identifier and password', 'danger')
    return render_template('enroll.html', title='Login', apt=apt, form=form)


@Indskrivning.route("/back")
def back():
    logout_user()
    return redirect(url_for('Indskrivning.home2'))


@Indskrivning.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Indskrivning.home2'))
    is_employee = True if request.args.get('is_employee') == 'true' else False
    form = EmployeeLoginForm() if is_employee else CustomerLoginForm()
    if form.validate_on_submit():
        user = select_Employees(form.id.data) if is_employee else select_Customers(form.id.data)
        if user != None and bcrypt.check_password_hash(user[2], form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Indskrivning.home2'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')
    return render_template('login.html', title='Login', is_employee=is_employee, form=form)


@Indskrivning.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Indskrivning.home2'))


@Indskrivning.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')



