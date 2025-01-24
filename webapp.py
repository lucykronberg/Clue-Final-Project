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

app.debug = False #Change this to False for production

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

@app.context_processor
def inject_logged_in():
    is_logged_in = 'github_token' in session
    return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')
    
    """, file_state=file_state"""

@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https')) #callback URL must match the pre-configured callback URL

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
        rrandom = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        random.shuffle(rrandom)
        doc = {"Username": username, "Murderer": murderer, "Target_place": target_place, "Weapon": weapon, "People": not_murderers, "Places": not_places, "Objects": not_weapons, "People_locations": rrandom}
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
        return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))
    username = session['user_data']['login']
    for doc in mongoUser_save.find({"Username":username}):
        hintS1 = doc["People"]
        hintR1 = doc["Places"]
        hintW1 = doc["Objects"]
        rrandom = doc["People_locations"]
        Suspects = ["adams", "tormey", "reussner", "barr", "jose", "lotze", "white", "white", "white"]
        murderer = doc["Murderer"]
        target_place = doc["Target_place"]
        weapon = doc["Weapon"]
    rherrings = ["I couldn’t see anything! The lights went out…and the next thing I know Mr. Al is dead!", "I’m not sure of anything anymore. Except for one thing, you can’t trust anyone around this school.", "I don’t know! One minute Mr. Al was here next to us… and the next he’s gone!", "This kind of publicity is going to ruin the school!", "I don’t what happened! All I do know is… I’m going to have to find a job at SM now. Bleh.", "The lights must’ve gone out because of the nearby fire. Poor Mr. Al."]
    mBarr = ["I could only see a dark silhouette, but I know for sure the murderer had long hair tied in the back and wore boots.", "The murderer wore blue…and I swore I heard murmurs of hate for war?", "I only got a quick glimpse of the murderer, but they were wearing a red collared shirt", "", "The murderer wore green, I’m sure of it. Weirdly also, I swore they had some dirt on them. Like actual dirt.", "The murderer looked tall, and blonde I think? I can’t really remember it all happened so fast."]
    mAdams = {"Quad": "I saw some shifty stuff going on in the quad, but it might have just been some afterschool band kids.", "Gym": "I was away from Mr. Al when it all happened. But I swear I heard his screams echo near the stadium.", "Hallway": "I thought I heard someone running just outside of the classrooms.", "Senior Lawn": "I could’ve sworn I saw grass stains on Mr. Al’s blazer when we found him…", "Cafeteria": "I heard something loud coming from the cafeteria. Better go check it out.", "VADA": "I found a trail of dirt all around the high school. Someone must’ve gone through the gardens…",  "CSA": "The murder occurred someplace very dark…in the rooms with no windows.", "Library": "I couldn’t hear anything. Wherever Mr. Al was murdered, it must’ve been quiet.", "Theater": "I heard I commotion in the theater right before the lights went out."}
    mReussner = {"Quad": "I definitely heard something going on outside in the Quad. I might need Murphy for some moral support…", "Gym": "I heard a scream from the gym…I didn’t think there was a home game today?", "Hallway": "Did you hear that noise out in the hallways, or was that just me?", "Senior Lawn": "I can’t believe someone would fall asleep on the senior lawn? Someone must’ve been up way past their bedtime...", "Cafeteria": "I didn’t think the school food was THAT bad…", "VADA": "Why is it always VADA involved in murder mysteries? The prom a couple years ago, and now this!", "CSA": "I swore I saw Mr. Stewart running for help. Something must’ve happened around him…", "Library": "Hold on, I need to use my think time…Mr. Al had talked about wanting to visit Mrs. Bryans earlier. I pretty sure.", "Theater": "Mr. Al was always in the spotlight, but I didn’t think he would die in it. This is not a boo yeah moment."}
    mJose = {"Quad": "I thought I saw something in the quad… or someone. Darwin, my beloved, is that you?", "Gym": "Are the dons winning? Who’s playing in the gym today?…oh.", "Hallway": "The only thing that’s REALLY being murdered right now is the climate. Although I think I did see something going on inside the school earlier.", "Senior Lawn": "At least a body’s nutrients will be good for soil? *cries*", "Cafeteria": "I knew there were too many GMOs in today’s meals!", "VADA": "Do crime scenes count as art?", "CSA": "We need to spend more time in nature and less around technology…Mr.Al sort of proves my point.", "Theater": "It’s a dramatic way to go, for sure. I’m sorry I can’t really talk right now."}
    mTormey = {"Wires": "Is this why I had trouble turning on the TV to show my slides today?", "Dr.Pepper": "I heard a pop and maybe a fizz? Riiiight before the screaming started…", "Calculator": "I heard clicking sounds before a scream. Clacking ones too if you will.", "Stapler": "Now my plays can’t be held together!", "Pencil": "You should be taking down notes.", "Barbie": "I’m so mad. First someone steals my Aztec death whistle now my Barbie. I was going to auction it!"}
    mLotze = {"Wires": "I’m pretty sure that’s in unit 4 of physics? We didn’t get to that though because of the block schedule.", "Calculator": "I swear students are always stealing my calculators.", "Dr.Pepper": "This murderer has taste!", "Stapler": "The murder weapon looked like a gun, but none of us were given anything like that…were we?", "Pencil": "It’s not LEAD it’s GRAPHITE people.", "Barbie": "I found a sample of the  murder weapon, which was made of polyvinyl chloride, or PVC. Total feta."}
    Possible_People = ["Mrs. Adams", "Tormey", "Mr. Reussner", "Mrs. Barr", "Jose", "Mr. Lotze"]
    Places = ["Quad", "Gym", "Hallway", "Senior Lawn", "Cafeteria", "VADA building", "CS academy", "Library", "Theater"]
    Objects = ["Wires", "Diet Dr Pepper", "Calculator", "Stapler", "Pencil", "Barbie"]
    Dialouge = []
    barr = mBarr[Possible_People.index(murderer)]
    adams = mAdams[Places.index(target_place)]
    reussner = mReussner[Places.index(target_place)]
    jose = mJose[Places.index(target_place)]
    tormey = mTormey[Objects.index(weapon)]
    lotze = mLotze[Objects.index(weapon)]
    Dialouge.append(adams)
    Dialouge.append(tormey) 
    Dialouge.append(reussner) 
    Dialouge.append(barr) 
    Dialouge.append(jose) 
    Dialouge.append(lotze)
    Dialouge[Possible_People.index(murderer)] = rherrings[random.randrange(0,6)]
    for x in range(3):
        Dialouge.append("") 
    RDialouge = []
    People = []
    for x in range(9):
        People.append(Suspects[rrandom[x]])
        RDialouge.append(Dialouge[rrandom[x]])
    return render_template('page1.html',dump_user_data=user_data_pprint,hintS1=hintS1[0],hintR1=hintR1[0],hintW1=hintW1[0],Place0=People[0],Place1=People[1],Place2=People[2],Place3=People[3],Place4=People[4],Place5=People[5],Place6=People[6],Place7=People[7],Place8=People[8],txt0=RDialouge[0],txt1 =RDialouge[1],txt2=RDialouge[2],txt3=RDialouge[3],txt4=RDialouge[4],txt5=RDialouge[5],txt6=RDialouge[6],txt7=RDialouge[7],txt8=RDialouge[8])
    
@app.route('/page2')
def renderPage2():
    if 'user_data' in session:
        user_data_pprint = pprint.pformat(session['user_data'])
    else:
        user_data_pprint = '';
        return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))
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
        outcome="solved the mystery! Play again to start a whole new one."
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
