from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from myproject import db
from werkzeug.security import generate_password_hash,check_password_hash
from myproject.models import User, Task 
from myproject.users.forms import RegistrationForm, LoginForm, UpdateUserForm



users = Blueprint('users', __name__)

#Register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


#Login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)



#Logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


#Account(Update Userform)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        #if form.picture.data:
            #username = current_user.username
            #pic = add_profile_pic(form.picture.data,username) #picture_handler.py
            #current_user.profile_image = pic #Model

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    #profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image) #default image
    return render_template('account.html',  form=form) 


#User's list of blog post
@users.route("/<username>")
@login_required
def user_tasks(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    tasks = Task.query.filter_by(author=user).order_by(Task.period, Task.status.desc()).paginate(page=page, per_page=10)
    return render_template('user_tasks.html', tasks=tasks, user=user)

