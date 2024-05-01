import sqlite3

def createUser(username, password, salt, bio="this is an empty bio"):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, salt, bio) VALUES (?, ?, ?, ?)", (username, password, salt, bio))
    conn.commit()
    conn.close()


def idAndBioIfCorrectPassword(username, hashedPassword):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT id, bio FROM users WHERE username = ? AND password = ?", (username, hashedPassword))
    idAndBioTupple = c.fetchone()
    conn.close()
    return idAndBioTupple if idAndBioTupple else None

def getSalt(username):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT salt FROM users WHERE username = ?", (username,))
    salt = c.fetchone()[0]
    conn.close()
    return salt

def usernameExists(username) -> bool:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    usernameExists = c.fetchone()
    conn.close()
    return bool(usernameExists)




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

def allUsers() -> dict[str, int]:
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT username, id FROM users")
    users = c.fetchall()
    conn.close()
    return dict(users)

usernameToIdDictOfAllUsers = allUsers()
print(f"{usernameToIdDictOfAllUsers = }")
