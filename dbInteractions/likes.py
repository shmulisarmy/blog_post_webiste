import sqlite3


db_name = "test.db"
def likeAPost(user_id, post_id) -> None:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
    conn.commit()
    conn.close()

def unlikeAPost(user_id, post_id) -> None:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("delete from likes where user_id = ? and post_id = ?", (user_id, post_id))
    conn.commit()
    conn.close()


def getAllLikedByUser(userId: int) -> list[tuple[int]]:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT post_id FROM likes WHERE user_id = ?", (userId,))
    posts = c.fetchall()
    conn.close()
    print(f"{posts = }")
    return posts


def getAllUsersThatLikedPost(post_id: int) -> list[tuple[int]]:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT user_id FROM likes WHERE post_id = ?", (post_id,))
    user_ids = c.fetchall()
    conn.close()
    print(f"{user_ids = }")
    return user_ids