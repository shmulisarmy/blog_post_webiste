from flask import blueprints, request, render_template, redirect, url_for, session

from dbInteractions.users import createUser, idAndBioIfCorrectPassword, followUser, unfollowUser, getAllFollowers, getAllFollowing, getSalt, usernameExists
from website.utils import hash, generateSalt, isCommonPassword

accounts_blueprint = blueprints.Blueprint("accounts", __name__, url_prefix="/")


@accounts_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        return render_template('signup.html', message='Please fill in all fields')
    
    if usernameExists(username):
        return render_template('signup.html', message='Username already exists')
    
    if isCommonPassword(password):
        return render_template('signup.html', message='Password is too common')
    
    if len(password) < 8:
        return render_template('signup.html', message='Password is too short')
    
    if len(password) > 64:
        return render_template('signup.html', message='Password is too long')
    
    if len(username) > 64:
        return render_template('signup.html', message='Username is too long')
    
    salt = generateSalt()
    saltedHash = hash(password, salt)
    bio = 'hello how are you doing'
    createUser(username, saltedHash, salt, bio)


    session['username'] = username
    session['bio'] = bio

    return render_template('home.html', message='Account created')
    
@accounts_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    print(f"message: {session = }")
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form["username"]
    password = request.form["password"]
    
    if not username or not password:
        return render_template('login.html', message='Please fill in all fields')
    
    salt = getSalt(username)

    hashedPassword = hash(password, salt)

    IdandBio = idAndBioIfCorrectPassword(username, hashedPassword)

    if not IdandBio:
        return render_template('login.html', message='wrong username or password')

    Id, bio = IdandBio
    
    session['id'] = Id
    session['bio'] = bio
    session['username'] = username
    

    return redirect(url_for('home'))


@accounts_blueprint.route('/logout')  
def logout():
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))
