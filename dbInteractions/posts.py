import sqlite3

def getAllPosts():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT title, summary, id FROM posts")
    posts = c.fetchall()
    print(f"{posts = }")
    conn.close()
    return posts


def returnsTitleToIdDictOfAllPosts():
    """"used for loading into search tree"""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT title, id FROM posts")
    posts = c.fetchall()
    print(f"{posts = }")
    conn.close()
    TitleToIdDictOfAllPosts = {post[0]: post[1] for post in posts}
    return TitleToIdDictOfAllPosts


TitleToIdDictOfAllPosts: dict = returnsTitleToIdDictOfAllPosts()


def createPost(title, summary, body, authorId):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO posts (user_id, title, summary, body) VALUES (?, ?, ?, ?)", (authorId, title, summary, body))
    conn.commit()
    conn.close()


def getPostById(id: int):
    print(f"getPost: {id}")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT title, summary, body FROM posts WHERE id = ?", (id,))
    post = c.fetchone()
    conn.close()
    print(f"{post = }")
    return post


def getPostByUserId(userId: int):
    print(f"getPost: {id}")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT author, title, body FROM posts WHERE user_id = ?", (userId,))
    post = c.fetchone()
    conn.close()
    print(f"{post = }")
    return post


db_name = "test.db"