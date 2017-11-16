import sqlite3

f="data/users.db"
#==========================================================

def validate(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    # print ("SELECT count(*) FROM users WHERE username = '%s' AND password = %s" % (username, password))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s' AND password = '%s'" % (username, password)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

def hasUsername(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    # print ("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s'" % (username)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

def newID():
    db = sqlite3.connect(f)
    c = db.cursor()
    # get the max id
    maxID = c.execute("SELECT MAX(id) FROM users").fetchall()
    db.commit()
    db.close()
    return maxID[0][0] + 1

def newStoryID():
    db = sqlite3.connect(f)
    c = db.cursor()
    # get the max id
    maxID = c.execute("SELECT MAX(storyid) FROM storylist").fetchall()
    db.commit()
    db.close()
    return maxID[0][0] + 1

def addUser(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('%s', '%s', '%s')" % (username, password, newID()))
    db.commit()
    db.close()

def getID(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    ids = c.execute("SELECT id FROM users WHERE username = '%s'" % (username)).fetchall()
    db.commit()
    db.close()
    return ids[0][0]

