import sqlite3



db_name = "test.db"

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


def getPostsByUserId(userId: int) -> list[tuple]:
    print(f"getPost: {id}")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT title, summary, id FROM posts WHERE user_id = ?", (userId,))
    posts = c.fetchall()
    conn.close()
    print(f"{posts = }")
    return posts

def getPostsByIds(post_ids: tuple[int]) -> list[tuple]:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT title, summary, id FROM posts WHERE id IN (" + ", ".join(str(i) for i in post_ids)+")")
    posts = c.fetchall()
    conn.close()
    print(f"{posts = }")
    return posts