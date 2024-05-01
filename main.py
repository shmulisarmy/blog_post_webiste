import logging.config
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from website.utils import generateSalt, hash, isCommonPassword
from colors import red, green

from dbInteractions.posts import createPost, getPostById, getAllPosts, getPostsByUserId, getPostsByUserId, getPostsByIds
from dbInteractions.users import createUser, idAndBioIfCorrectPassword, followUser, unfollowUser, getAllFollowers, getAllFollowing, getSalt, usernameExists
from dbInteractions.likes import likeAPost, unlikeAPost, getAllLikedByUser, getAllUsersThatLikedPost
from search.load import postTitleToIdTree
from blueprints.accounts import accounts_blueprint

app = Flask(__name__)
app.register_blueprint(accounts_blueprint)
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
    return render_template('main.html', blog=blog, id=index)


@app.route('/home')
def home():
    user_id = session.get('id')
    username = session.get('username')
    print(f"{user_id = } {username = }")

    if not user_id:
        return redirect(url_for('login'))
    blogs = []
    for usersId_intuples in getAllFollowing(user_id):
        usersId = usersId_intuples[0]
        print(f"following: {usersId = }")
        for blog in getPostsByUserId(usersId):
            blogs.append(blog)
    return render_template('home.html', blogs=blogs, bio=session.get('bio'), username=username)


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


@app.route('/myPosts')
def myPosts():
    if 'id' not in session:
        return redirect(url_for('login'))
    print(f"{session['id'] = }")
    return render_template('myPosts.html', username=session['username'], blogs=getPostsByUserId(session['id']))



"""htmx search"""
@app.route('/searchResults', methods=['GET', 'POST'])
def searchResults():
    if __debug__:
        print(f"tree = {list(filter(lambda x: callable(x), dir(postTitleToIdTree)))} {dir(postTitleToIdTree) = }")
        print(f"{postTitleToIdTree = }")
    searchLetters = request.form.get('searchLetters')
    print(f"{searchLetters = }")
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





@app.route('/likePost', methods=['POST'])
def likePost():
    user_id = session.get('id')
    post_id = request.form.get('post_id')
    print(f"{user_id = } {post_id = }")
    if user_id and post_id:
        likeAPost(user_id, post_id)

    return "success"


@app.route('/unlikePost', methods=['POST'])
def unlikePost():
    user_id = session.get('id')
    post_id = request.form.get('post_id')
    if not (user_id and post_id):
        return "failed"
    unlikeAPost(user_id, post_id)
    return "success"


@app.route('/likedByUser', methods=['GET'])
def likedByUser():
    user_id = session.get('id')
    if not user_id:
        return "failed"
    liked_by_user = getAllLikedByUser(user_id)
    return getPostsByIds(liked_by_user)
    # return render_template('likedByUser.html', liked_by_user=liked_by_user)


@app.route('/usersLikedPost/<int:post_id>', methods=['GET'])
def usersLikedPost(post_id):
    users_liked_post = getAllUsersThatLikedPost(post_id)
    return users_liked_post
    # return render_template('usersLikedPost.html', users_liked_post=users_liked_post)





if __name__ == '__main__':
    print(f"go to {green('http://localhost:4040/home')}")
    app.run(debug=True, port=4040)