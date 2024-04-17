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
