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
import json 
 
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
    if "user_data" in session:
        new_document()
    """username = session['user_data']['login']
    user = mongoUser_save.find_one({"Username":username})
    if user == None:
        file_state = "start"
    else: 
        file_state = "resume"""
    return render_template('home.html')
    
    """, file_state=file_state"""

@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='http')) #callback URL must match the pre-configured callback URL

@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out.')
    return redirect('/')
    
@app.route('/new_document')
def new_document():
    username = session['user_data']['login']
    user = mongoUser_save.find_one({"Username":username})
    if user == None:
        People = ["Mrs. Adams", "Tormey", "Mr. Reussner", "Mrs. Barr", "Jose", "Mr. Lotze"]
        murderer = random.choice(People)
        People.remove(murderer)
        Places = ["Quad", "Gym", "Hallway", "Senior Lawn", "Cafeteria", "VADA building", "CS academy", "Library", "Theater"]
        target_place = random.choice(Places)
        Places.remove(target_place)
        Objects = ["Wires", "Diet Dr Pepper", "Calculator", "Stapler", "Pencil", "Barbie"]
        weapon = random.choice(Objects)
        Objects.remove(weapon)
        not_murderers = []
        not_places = []
        not_weapons = []
        for x in range(2):
            not_murderers.append(random.choice(People))
            People.remove(not_murderers[x])
            not_places.append(random.choice(Places))
            Places.remove(not_places[x])
            not_weapons.append(random.choice(Objects))
            Objects.remove(not_weapons[x])
        random = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        random.shuffle(random)
        doc = {"Username": username, "Murderer": murderer, "Target_place": target_place, "Weapon": weapon, "People": not_murderers, "Places": not_places, "Objects": not_weapons, "People_locations": random}
        mongoUser_save.insert_one(doc)       
    return render_template('home.html')

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
            new_document()
            """username = session['user_data']['login']
            user = mongoUser_save.find_one({"Username":username})
            if user == None:
                People = ["Mrs. Adams", "Tormey", "Mr. Reussner", "Mrs. Barr", "Jose", "Mr. Lotze"]
                murderer = random.choice(People)
                People.remove(murderer)
                Places = ["Quad", "Gym", "Hallway", "Senior Lawn", "Cafeteria", "VADA building", "CS academy", "Library", "Theater"]
                target_place = random.choice(Places)
                Places.remove(target_place)
                Objects = ["Wires", "Diet Dr Pepper", "Calculator", "Stapler", "Pencil", "Barbie"]
                weapon = random.choice(Objects)
                Objects.remove(weapon)
                not_murderers = []
                not_places = []
                not_weapons = []
                for x in range(2):
                    not_murderers.append(random.choice(People))
                    People.remove(not_murderers[x])
                    not_places.append(random.choice(Places))
                    Places.remove(not_places[x])
                    not_weapons.append(random.choice(Objects))
                    Objects.remove(not_weapons[x])
                doc = {"Username": username, "Murderer": murderer, "Target_place": target_place, "Weapon": weapon, "People": not_murderers, "Places": not_places, "Objects": not_weapons}
                mongoUser_save.insert_one(doc)"""
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
    username = session['user_data']['login']
    for doc in mongoUser_save.find({"Username":username}):
        hintS1 = doc["People"]
        hintR1 = doc["Places"]
        hintW1 = doc["Objects"]
        random = doc["People_locations"]
        Suspects = ["adams", "tormey", "reussner", "barr", "jose", "lotze", "white", "white", "white"]
        People = []
        for x in range(9):
            People.append(Suspects[random[x]])
    return render_template('page1.html',dump_user_data=user_data_pprint,hintS1=hintS1[0],hintR1=hintR1[0],hintW1=hintW1[0],Place0=People[0],Place1=People[1],Place2=People[2],Place3=People[3],Place4=People[4],Place5=People[5],Place6=People[6],Place7=People[7],Place8=People[8])

@app.route('/page2')
def renderPage2():
    if 'user_data' in session:
        user_data_pprint = pprint.pformat(session['user_data'])
    else:
        user_data_pprint = '';
        return github.authorize(callback=url_for('authorized', _external=True, _scheme='http'))
    return render_template('page2.html')

@github.tokengetter
def get_github_oauth_token():
    return session['github_token']
    
@app.route('/page3', methods=["GET","POST"])
def renderPage3():
    Suspect= request.form ["Suspect"]
    Weapon= request.form ["Weapon"]
    Room= request.form ["Room"]
    
    correctSuspect= ""
    correctWeapon= ""
    correctRoom= ""
    
    username = session['user_data']['login']
    for doc in mongoUser_save.find({"Username":username}):
        correctSuspect = doc["Murderer"]
        correctRoom = doc["Target_place"]
        correctWeapon = doc["Weapon"]
  
    outcome=""
    repeat=""
    if Suspect==correctSuspect and Weapon==correctWeapon and Room==correctRoom:
        outcome="solved the mystery!"
        repeat="Play again"
    else:
        outcome="failed! The murderer is still out there..."
        repeat="Try again"
     
    return render_template('page3.html', outcome=outcome, repeat=repeat)
    
@app.route('/new_game')
def new_game():
    username = session['user_data']['login']
    user = mongoUser_save.find_one({"Username":username})
    mongoUser_save.delete_one({"Username":username})
    new_document()
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run()
