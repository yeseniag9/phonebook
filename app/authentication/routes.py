from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user) # Like git
            db.session.commit()  # Like git

            flash(f'You have successfully created a user account {email}', 'User-created') # Like a pop-up window; 'User-created' is there to talk to our application
            return redirect(url_for('site.home'))
    except: 
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST']) # The browser uses methods to cetegorize the way it handles data
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password): # Checking if the login was the right credentials
                login_user(logged_user)
                flash('You were successful in your initiation. Congratulations, and welcome to the Jedi Knights', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
                return redirect(url_for('auth.signin')) # ** url_for means we can tell flask to return the html for a certain file without having to call a method; we can just tell it to figure out what the url is to locate the document
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))