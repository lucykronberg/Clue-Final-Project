from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash
from flask_oauthlib.client import OAuth
from markupsafe import Markup
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from bson.objectid import ObjectId

import pprint
import os
import time
import pymongo
import sys
import random
 
app = Flask(__name__)

app.debug = True #Change this to False for production

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Remove once done debugging

app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies
oauth = OAuth(app)
oauth.init_app(app) 

github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web app's "username" for github's OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],#your web app's "password" for github's OAuth
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)

connection_string = os.environ["MONGO_CONNECTION_STRING"]
user_infodb_name = os.environ["MONGO_DBNAME"]

client = pymongo.MongoClient(connection_string)
user_savedb = client[user_infodb_name]
mongoUser_save = user_savedb['User_save']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='http')) #callback URL must match the pre-configured callback URL

@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out.')
    return redirect('/')

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        flash('Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args), 'error')      
    else:
        try:
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            session['user_data']=github.get('user').data
            username = session['user_data']['login']
            user = mongoUser_save.find_one({"Username":username})
            if user == None:
                People = ["Mrs. Adams", "Tormey", "Mr. Reussner", "Mrs. Barr", "Jose", "Mr. Lotze"]
                murderer = random.choice(People)
                Places = ["Quad", "Gym", "Hallway", "Senior Lawn", "Cafeteria", "VADA building", "CS academy", "Library", "Theater"]
                target_place = random.choice(Places)
                Object = ["Wires", "Ruler", "Calculator", "Stapler", "Pencil", "Barbie"]
                weapon = random.choice(Object)
                doc = {"Username": username, "Murderer": murderer, "Target_place": target_place, "Weapon": weapon, "People": [""], "Places": [""], "Objects": [""]}
                mongoUser_save.insert_one(doc)
            message = 'You were successfully logged in as ' + session['user_data']['login'] + '.'
        except Exception as inst:
            session.clear()
            print(inst)
            message = 'Unable to login, please try again.', 'error'
    return render_template('message.html', message=message)


@app.route('/page1')
def renderPage1():
    if 'user_data' in session:
        user_data_pprint = pprint.pformat(session['user_data'])
    else:
        user_data_pprint = '';
        return github.authorize(callback=url_for('authorized', _external=True, _scheme='http'))
    return render_template('page1.html',dump_user_data=user_data_pprint)

@app.route('/page2')
def renderPage2():
    return render_template('page2.html')

#the tokengetter is automatically called to check who is logged in.
@github.tokengetter
def get_github_oauth_token():
    return session['github_token']
    
@app.route('/page3', methods=["GET","POST"])
def renderPage3():
    
    Suspect= request.form["Suspect"]
    Weapon= request.form["Weapon"]
    Room= request.form["Room"]
    print(Suspect)
    print(Weapon)
    print(Room)
    
    correctSuspect= ""
    correctWeapon= ""
    correctRoom= ""
    username = session['user_data']['login']
    for doc in mongoUser_save.find({"Username":username}):
        correctSuspect = doc["Murderer"]
        correctRoom = doc["Target_place"]
        correctWeapon = doc["Weapon"]
        print(correctSuspect)
        print(correctWeapon)
        print(correctRoom)
  
    outcome=""
    repeat=""
    if Suspect==correctSuspect and Weapon==correctWeapon and Room==correctRoom:
        outcome="solved the mystery!"
        repeat="Play again"
    else:
        outcome="failed! The murderer is still out there..."
        repeat="Try again"
     
    return render_template('page3.html', outcome=outcome, repeat=repeat)

if __name__ == '__main__':
    app.run()
