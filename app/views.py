"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os 
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import ProfileForm, LoginForm
from app.models import UserProfile
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import datetime 


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    # Instantiate your form class
    if request.method == 'GET':
        form = ProfileForm()
        return render_template('profile.html', form = form)

    # Validate file upload on submit
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Get file data and save to your uploads folder
        F_Name = form.F_Name.data
        L_Name =  form.L_Name.data
        Username = form.Username.data
        Password = form.Password.data
        Gender = form.Gender.data
        Email = form.Email.data
        Location = form.Location.data
        Biography = form.Biography.data
        file = form.file.data
        filename = secure_filename(file.filename)
        print("Check1")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        profile = UserProfile(F_Name,L_Name,Username,Password,Gender,Email,Location,Biography,filename,datetime.datetime.now().strftime("%B %d, %Y"))
        db.session.add(profile)
        db.session.commit()
        print("Check2")
        flash('Profile Added', 'success')
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profileuserid', userid = user.id))


    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():

        Username = form.Username.data
        Password = form.Password.data
        user = UserProfile.query.filter_by(Username=Username).first()

        if user is not None and check_password_hash(user.Password, Password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

            login_user(user, remember=remember_me)

            flash('Logged in successfully.', 'success')

            return redirect(url_for('profileuserid', userid = user.id))
        else:
            flash('Username or Password is incorrect.', 'danger')

    return render_template('login.html', form=form)


@app.route('/profileuserid/<int:userid>')
def profileuserid(userid):
    profile = UserProfile.query.filter_by(id=userid).first()
    return render_template('profileuserid.html', profile = profile)
@app.route('/secure-page')
@login_required
def secure_page():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('secure_page.html')

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))



# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###



@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
