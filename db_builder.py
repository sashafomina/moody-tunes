import sqlite3, hashlib   #enable control of an sqlite database

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
def table_gen():
    create_users = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER)"
    c.execute(create_users)


def default():
    # commands do not run unless it is the start
    # really not necessary unless someone wants to run db_builder more than once...
    for status in c.execute("SELECT count(*) FROM users WHERE username = 'admin' AND password = 'password'"):
        if(status[0] != 1):
            hash_obj = hashlib.sha256('password')
            hex_dig = hash_obj.hexdigest()
            c.execute("INSERT INTO users VALUES('%s', '%s', 0)" % ('admin', hex_dig))
            return
              
table_gen()
default()
#==========================================================
db.commit() #save changes
db.close() #close database
