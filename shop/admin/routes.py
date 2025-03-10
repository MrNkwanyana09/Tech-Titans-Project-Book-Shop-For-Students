from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db
from .forms import RegistrationForm, LoginForm
from .models import User

#@app.route('/')
#def home():
 #   return "Home Page Of Your Shop"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = (form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                   password=hash_password)
        db.session.add(user)
        db.session.commit()  # Commit the transaction
        flash('Thanks for registering')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} You are successfully logged in', 'success')
            return redirect(request.args.get('next') or url_for('home'))  # Changed 'admin' to 'home'
        else:
            flash('Wrong Password Please try again', 'danger')
    return render_template('admin/login.html', form=form, title="Login page")

