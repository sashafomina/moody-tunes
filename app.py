from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3, hashlib, uuid
from datetime import datetime
from utils import api_library, dbLibrary
import json


def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest() + ':' + key

def check_password(hashed_password, user_password):
    password,key = hashed_password.split(":")
    return password == hashlib.sha256(key.encode() + user_password.encode()).hexdigest()


tunes_app = Flask(__name__)
tunes_app.secret_key = os.urandom(32)

#----------------------HOME PAGE-------------------------------

@tunes_app.route("/")
def root():
    return render_template("home.html")

#------------------------LOGIN----------------------------------

@tunes_app.route("/login", methods = ['POST' , 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('diary'))
    return render_template("login.html")

@tunes_app.route("/authenticate",methods = ['POST','GET'])
def authenticate():
    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)
    input_username = request.form['username']
    input_password = request.form['password']

    if input_username=='' or input_password=='' :
        flash("Please Fill In All Fields")
        return redirect(url_for('login'))

    if "'" in input_username or "'" in input_password:
        flash("Invalid Login Info")
        return redirect(url_for('login'))

    hashed_passCursor = cursor.execute("SELECT password FROM users WHERE username = '" + input_username + "'")
    numPasses = 0 #should end up being 1 if all fields were filled

    for item in hashed_passCursor:
        numPasses += 1
        hashed_pass = item[0]
        print item[0]

    dbLibrary.closeFile(dbTunes)

    if  numPasses == 0:
        flash ("User doesn't exist")
        return redirect(url_for('login'))

    elif check_password(hashed_pass, input_password):
        flash("Login Successful")
        session["username"] = input_username;#in order to keep track of user
        return redirect(url_for('diary'))

    else:
        flash("Invalid Login Information")
        return redirect(url_for('login'))


#-------------------------------------------------------------------



#---------------CREATING AN ACCOUNT----------------------------------
@tunes_app.route("/account", methods = ['POST' , 'GET'])
def account():
    return render_template("register.html")

@tunes_app.route("/accountSubmit", methods = ['POST' , 'GET'])
def accountSubmit():
    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)
    #print request.form
    username = request.form['newUsername']
    password = request.form['newPassword']

    if username == '' or password == '':
        dbLibrary.closeFile(dbTunes)
        flash("Please Fill In All Fields")
        return redirect(url_for('account'))

    elif len(password)< 6:
        dbLibrary.closeFile(dbTunes)
        flash("Password must have at least 6 characters")
        return redirect(url_for('account'))

    elif (' ' in username or ' ' in password or "'" in username or "'" in password or '"' in username or '"' in password ):
        dbLibrary.closeFile(dbTunes)
        flash("Username and Password cannot contain the space,single quote, or double quote character")
        return redirect(url_for('account'))

    password = hash_password(password)
    sameUser = cursor.execute("SELECT username FROM users WHERE username = '" + username +"'")

    counter = 0 #should remain 0 if valid username since username needs to be unique
    for item in sameUser:
        counter += 1

    if counter == 0:
        dbLibrary.insertRow('users',['username', 'password', 'sadness', 'joy', 'anger', 'fear'],[username, password, "base", "base", "base", "base"],cursor)
        flash("Account Successfully Created")
        dbLibrary.commit(dbTunes)
        dbLibrary.closeFile(dbTunes)
        return redirect(url_for('login'))

    else:
        flash("Invalid: Username taken")
        dbLibrary.commit(dbTunes)
        dbLibrary.closeFile(dbTunes)
        return redirect(url_for('account'))

#-----------------------------------------------------------

#----------------DIARY HOME---------------------------------
@tunes_app.route("/diary", methods = ['POST' , 'GET'])
def diary():
    if 'username' not in session:
        flash("Session timed out")
        return redirect(url_for('login'))
    current_user = session["username"]

    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)
    entry_cursor = cursor.execute("SELECT entry,mood, date, song, songRating FROM diary WHERE username = '" + current_user + "';")
    entries = cursor.fetchall()

    song_artist_cursor = cursor.execute("SELECT diary.song, artist FROM diary,songs WHERE username = '" + current_user+ "' and songs.song=diary.song;")

    info = []
    for item in song_artist_cursor:
        sublist= []
        sublist.append(item[1])
        sublist.append(api_library.get_link(item[0],item[1]))
        info.append(sublist)
    counter = 0

    for data in info:
        subCounter = 0
        for stuff in entries:
            if counter == subCounter:
                data.append(stuff[0]) #entry index 2
                data.append(stuff[1]) #mood 3
                data.append(stuff[2]) #date 4
                data.append(stuff[3]) #song 5
                if stuff[4] == "two": #rate 6
                    data.append(["", "active" , ""])
                    data.append(["", "checked" , ""])
                elif stuff[4] == "one":
                    data.append(["active", "", ""])
                    data.append(["checked", "" , ""])
                else:
                    data.append(["", "", "active"])
                    data.append(["", "" , "checked"])
                 
            subCounter += 1
        counter += 1
                
            
    print info

    
    
    dbLibrary.closeFile(dbTunes)
    return render_template("diary.html",name = current_user, diary = info)

#---------------CREATING A NEW ENTRY----------------------
@tunes_app.route("/create", methods = ['POST' , 'GET'])
def create():
    if 'username' not in session:
        flash("Session timed out")
        return redirect(url_for('login'))
    current_user = session["username"] 

    new_entry = request.form['newDiaryEntry']

    d_tone = api_library.analyze_tone(new_entry)

    max_mood = (api_library.primary_tone(d_tone)).lower()
    #print max_mood

    if max_mood == "disgust":
        max_mood = "anger"

    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)

    recent_song_cursor = cursor.execute("SELECT " + max_mood + " FROM users WHERE username ='" + current_user +"';")
    for item in recent_song_cursor:
        recent_song = item

    recent_song = recent_song[0]


    #print recent_song == "base"      
    #print recent_song

    if recent_song == "base":
        song_rec_cursor = cursor.execute("SELECT song FROM songs WHERE parentSong = 'base' and mood = '" + max_mood + "';")
        song_rec = ""
        for item in song_rec_cursor:
            for song in item:
                song_rec = song
            dbLibrary.update("users", max_mood, "'" + song_rec + "'", "username = '" + current_user + "'", cursor)

   
    else:
        rating_cursor = cursor.execute("SELECT songRating FROM diary WHERE username = '" + current_user + "' and song = '" + recent_song + "' and mood = '" + max_mood + "';" )
        for item in rating_cursor:
            rating = item[0]

        song_rec_cursor =  cursor.execute("SELECT " + rating + " FROM songs WHERE mood = '" + max_mood + "' and song = '" + recent_song + "';");
        for item in song_rec_cursor:
            song_rec = item[0]
            #print song_rec

        artist_cursor = cursor.execute("SELECT artist FROM songs WHERE song = '" + recent_song + "';")
        for item in artist_cursor:
            artist = item[0]
            
        if song_rec is None:
            song_rec_list = api_library.get_child_songs(rating, recent_song, artist)
            song_rec =  song_rec_list[0] 
            new_artist = song_rec_list[1]
            dbLibrary.insertRow("songs" , ['song','artist','mood','parentSong'], [song_rec, new_artist, max_mood, recent_song], cursor)

    
    

    datetime2 = str(datetime.now())[0:-7]#date and time (w/o milliseconds)
    
    dbLibrary.insertRow("diary" , ["username" , "date" , "entry" , "mood" , "song" , "songRating"] , [current_user ,datetime2, new_entry, max_mood, song_rec, "two"], cursor)

    dbLibrary.commit(dbTunes)
    dbLibrary.closeFile(dbTunes)

    
    return redirect(url_for("diary"))

#------------------RATE---------------------------------
@tunes_app.route("/rate" , methods = ['GET' , 'POST'])
def rate():
    dbTunes = dbLibrary.openDb("data/tunes.db")
    cursor = dbLibrary.createCursor(dbTunes)

    current_user = session["username"]
    new_rating = "'" + request.form['options'] + "'"

    dbLibrary.update("diary", "songRating", new_rating, "username = '" + current_user + "'", cursor)  

    dbLibrary.commit(dbTunes)
    dbLibrary.closeFile(dbTunes)

    return redirect(url_for("diary"))
#--------------------------------------------------------

#---------------------MISC-------------------------------
@tunes_app.route('/info', methods=['GET'])
def info():
    return render_template("info.html")

@tunes_app.route('/credits', methods=['GET'])
def credits():
    
    return render_template("credits.html")
#--------------------------------------------------------

#---------------------LOGGING OUT------------------------
@tunes_app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        flash("Logged out.")
    return redirect(url_for("root"))

#--------------------------------------------------------

if __name__ == '__main__':
    tunes_app.debug = True
    tunes_app.run()
