from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3, hashlib
import db_func

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

#========================LOGIN/ACCOUNT STUFF============================
@my_app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('home.html')

@my_app.route("/login", methods =['GET','POST'])
def login():
    if 'user' in session:
        ID = db_func.getID(session['user'])
    else:
        if (request.method == 'GET'):
            return render_template('login.html')
        else:
            username = request.form["username"]
            password = request.form["password"]
            hash_obj = hashlib.sha256(password)
            hex_dig = hash_obj.hexdigest()
            status = db_func.validate(username, hex_dig)
            if status:
                session["user"] = username
                return render_template("diary.html")
            elif db_func.hasUsername(username):
                flash("Incorrect credentials.")
            else:
                flash("Username does not exist.")
            return redirect(url_for('login'))
        
@my_app.route('/register', methods=['GET','POST'])
def register():
    if (request.method == 'POST'):
        username = request.form["newUsername"]
        password = request.form["newPassword"]
        repeat = request.form["repeatPassword"]
        if(password != repeat):
            flash("Passwords do not match.")
        else:
            if db_func.hasUsername(username):
                flash("Username taken.")
            else:
                hash_obj = hashlib.sha256(password)
                hex_dig = hash_obj.hexdigest()
                db_func.addUser(username, hex_dig)
                flash("Your account has been registered.")
                return redirect(url_for("login"))
    return render_template("register.html")

@my_app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        flash("Logged out.")
    return redirect(url_for('login'))

@my_app.route('/callback', methods=['GET'])
def callback():
    return redirect(url_for('login'))
#=======================================================================

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
