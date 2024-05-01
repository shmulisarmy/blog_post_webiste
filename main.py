import logging.config
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from website.utils import generateSalt, hash, isCommonPassword
from colors import red, green

from dbInteractions.posts import createPost, getPostById, getAllPosts, getPostByUserId
from dbInteractions.users import createUser, idAndBioIfCorrectPassword, followUser, unfollowUser, getAllFollowers, getAllFollowing
from search.load import postTitleToIdTree

app = Flask(__name__)
app.secret_key = b'\x1b\x7f\x0b\xca\x1c\x9d\xa9\xbd\x8a\x1f\x9b\x1b\xcb\x1c\x9d\xa9\xbd\x8a\x1f\x9b'

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return render_template('test.html')
    if request.method == 'POST':
        print(request.form)
        return request.form


@app.route('/<int:index>')
def index(index: int):
    blog = getPostById(index)
    print(f"{blog = }")
    return render_template('main.html', blog=blog)


@app.route('/home')
def home():
    return render_template('home.html', blogs=getAllPosts(), bio=session.get('bio'), username=session.get('username'))


@app.route('/createBlog', methods=['GET', 'POST'])
def createBlog():
    id = session.get('id')
    if not id:
        print(red(f""))
        return redirect(url_for('login'))
    

    if request.method == 'GET':
        return render_template('createBlog.html')
    
    title = request.form['title']
    summary = request.form['summary']
    body = request.form['body']

    if not title or not summary or not body:
        return redirect(url_for('createBlog'), message='Please fill in all fields')
    
    createPost(title, summary, body, id)
    return redirect(url_for('home'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
    
#     username = request.form["username"]
#     password = request.form["password"]
    
#     if not username or not password:
#         flash('Please fill in all fields')
#         return redirect(url_for('login'))
    
#     session['username'] = username
#     return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        return redirect(url_for('signup'), message='Please fill in all fields')
    
    if isCommonPassword(password):
        return redirect(url_for('signup'), message='Password is too common')
    
    if len(password) < 8:
        return redirect(url_for('signup'), message='Password is too short')
    
    if len(password) > 64:
        return redirect(url_for('signup'), message='Password is too long')
    
    if len(username) > 64:
        return redirect(url_for('signup'), message='Username is too long')
    
    salt = generateSalt()
    saltedHash = hash(password, salt)
    createUser(username, saltedHash, salt)

    return render_template('home.html', message='Account created')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(f"message: {session = }")
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form["username"]
    password = request.form["password"]
    
    if not username or not password:
        return render_template('login.html', message='Please fill in all fields')
    
    IdandBio = idAndBioIfCorrectPassword(username, password)

    if not IdandBio:
        return render_template('login.html', message='wrong username or password')

    Id, bio = IdandBio
    
    session['id'] = Id
    session['bio'] = bio
    session['username'] = username
    

    return redirect(url_for('home'))


@app.route('/logout')  
def logout():
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/myPosts')
def myPosts():
    if 'id' not in session:
        return redirect(url_for('login'))
    return render_template('myPosts.html', username=session['username'], blogs=getPostByUserId(session['id']))



"""htmx search"""
@app.route('/searchResults', methods=['GET', 'POST'])
def searchResults():
    if __debug__:
        print(f"tree = {list(filter(lambda x: callable(x), dir(postTitleToIdTree)))} {dir(postTitleToIdTree) = }")
        print(f"{postTitleToIdTree = }")
    searchLetters = request.form.get('searchLetters')
    print(f"{searchLetters = }")
    # searchResults = postTitleToIdTree.firstNThatStartWith(searchLetters, 5)
    searchResults = postTitleToIdTree.valueSearch(3, searchLetters)
    if searchResults:
        return render_template('searchResults.html', searchResults=searchResults)





@app.route('/follow', methods=['POST'])
def follow():
    user_id = session.get('id')
    follow_id = request.form.get('follow_id')
    if user_id and follow_id:
        #db func
        followUser(user_id, follow_id)

    return "success"

@app.route('/unfollow', methods=['POST'])
def unfollow():
    user_id = session.get('id')
    follow_id = request.form.get('unfollow_id')
    if not (user_id and follow_id):
        return "failed"
    unfollowUser(user_id, follow_id)
    return "success"


@app.route('/followers', methods=['POST'])
def followers():
    user_id = session.get('id')
    if not user_id:
        return "failed"
    followers = getAllFollowers(user_id)
    return render_template('followers.html', followers=followers)


@app.route('/following', methods=['POST'])
def following():
    user_id = session.get('id')
    if not user_id:
        return "failed"
    following = getAllFollowing(user_id)
    return render_template('following.html', following=following)






if __name__ == '__main__':
    app.run(debug=True, port=4040)