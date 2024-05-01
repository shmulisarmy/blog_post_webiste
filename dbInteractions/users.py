import sqlite3

def createUser(username, password, salt, bio="this is an empty bio"):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, salt, bio) VALUES (?, ?, ?, ?)", (username, password, salt, bio))
    conn.commit()
    conn.close()


def idAndBioIfCorrectPassword(username, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT id, bio FROM users WHERE username = ? AND password = ?", (username, password))
    idAndBioTupple = c.fetchone()
    conn.close()
    return idAndBioTupple if idAndBioTupple else None






"""followers table"""

def followUser(followerId, followingId) -> None:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO followers (user, follower) VALUES (?, ?)", (followerId, followingId))
    conn.commit()
    conn.close()


def unfollowUser(followerId, followingId) -> None:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("DELETE FROM followers WHERE user = ? AND follower = ?", (followerId, followingId))
    conn.commit()
    conn.close()


def getAllFollowers(userId)  -> list[int]:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT follower FROM followers WHERE user = ?", (userId,))
    followers = c.fetchall()
    conn.close()
    return followers


def getAllFollowing(userId) -> list[int]:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT user FROM followers WHERE follower = ?", (userId,))
    following = c.fetchall()
    conn.close()
    return following