from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///logins'

app.app_context().push()

app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SECRET_KEY'] = 'oh-so-secret'

connect_db(app)

toolbar = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def view_homepage():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def create_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = str(user.id)
        flash(f'Added {username}')
        return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome back, {username}!')
            session['user_id'] = str(user.id)
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Bad username/password']
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def view_userpage(username):
    if 'username' not in session:
        flash('Please login first!')
        return redirect('/login')
    else:
        user = User.query.filter(User.username == username).first()
    if user:
        id_str = str(user.id)
    else:
        flash('Invalid User!')
        if 'user_id' in session:
            return redirect('/')
        return redirect('/login')    
    if 'user_id' not in session:    
        flash('Please login first!')
        return redirect('/login')
    if id_str not in session['user_id']:
        flash('Unauthorized access!')
        return redirect('/')
    return render_template('users.html', user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    user = User.query.filter(User.username == username).first()
    id_str = str(user.id)
    if id_str not in session['user_id']:
        flash('Please login first!')
        return redirect('/login')    
    session.pop('user_id')
    session.pop('username')
    db.session.delete(user)
    db.session.commit() 
    flash('User had been deleted!')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):
    user = User.query.filter(User.username == username).first()
    id_str = str(user.id)    
    if 'user_id' not in session:    
        flash('Please login first!')
        return redirect('/login')
    if id_str not in session['user_id']:
        flash('Unauthorized access!')
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(feedback)
        db.session.commit()
        flash(f'Feedback added!')
        return redirect(f'/users/{username}')
    return render_template('feedback.html', user=user, form=form)

@app.route('/feedback/<id>/delete', methods=['POST'])
def delete_feedback(id):
    post = Feedback.query.get_or_404(id)
    id_str = str(post.user.id)    
    if 'user_id' not in session:    
        flash('Please login first!')
        return redirect('/login')
    if id_str not in session['user_id']:
        flash('Unauthorized access!')
        return redirect('/')
    db.session.delete(post)
    db.session.commit()
    flash('Feedback deleted!')
    return redirect(f'/users/{post.username}')

@app.route('/feedback/<id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    post = Feedback.query.get_or_404(id)
    id_str = str(post.user.id)    
    if 'user_id' not in session:    
        flash('Please login first!')
        return redirect('/login')
    if id_str not in session['user_id']:
        flash('Unauthorized access!')
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash('Feedback updated!')
        return redirect(f'/users/{post.username}')
    return render_template('/edit-feedback.html', post=post, form=form)

# @app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
# def feedback(username):
#     user = User.query.filter(User.username == username).first()
#     id_str = str(user.id)    
#     if 'user_id' not in session:    
#         flash('Please login first!')
#         return redirect('/login')
#     if id_str not in session['user_id']:
#         flash('Unauthorized access!')
#         return redirect('/')
#     form = FeedbackForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         content = form.content.data
#         feedback = Feedback(title=title, content=content, username=user.username)
#         db.session.add(feedback)
#         db.session.commit()
#         flash(f'Feedback added!')
#         return redirect(f'/users/{username}')
#     return render_template('feedback.html', user=user, form=form)

@app.route('/logout')
def logout():
    session.pop('user_id')    
    if 'username' in session:
        session.pop('username')    
    flash('Now logged out!')
    return redirect('/')

# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data

#         user = User.authenticate(username, password)
#         if user:
#             flash(f'Welcome back, {username}!')
#             session['user_id'] = str(user.id)
#             return redirect(f'/users/{username}')
#         else:
#             form.username.errors = ['Bad username/password']
#     return render_template('login.html', form=form)