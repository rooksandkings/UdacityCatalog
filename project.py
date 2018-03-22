from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, SpaceXLaunchManifest, Launches, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "SpaceX Launch-Manifest"


# Connect to Database and create database session
engine = create_engine('sqlite:///spaceXlaunchmanifestwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Manifest Information
@app.route('/launch_manifest/<int:manifest_id>/launch/JSON')
def manifestLaunchJSON(manifest_id):
    manifest = session.query(SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    launches = session.query(Launches).filter_by(
        launch_id=manifest_id).all()
    return jsonify(launches=[i.serialize for i in launches])


@app.route('/launch_manifest/<int:manifest_id>/launch/<int:launch_id>/JSON')
def launchJSON(manifest_id, launch_id):
    launch = session.query(Launches).filter_by(id=launch_id).one()
    return jsonify(launch=launch.serialize)


@app.route('/launch_manifest/JSON')
def manifestJSON():
    manifest = session.query(SpaceXLaunchManifest).all()
    return jsonify(manifest=[i.serialize for i in manifest])


# Show full manifest
@app.route('/')
@app.route('/launch_manifest/')
def showManifest():
    manifest = session.query(SpaceXLaunchManifest).order_by(asc(SpaceXLaunchManifest.name))
    return render_template('launch_manifest.html', manifest=manifest)


# Add a mission to the manifest
@app.route('/launch_manifest/new/', methods=['GET', 'POST'])
def newMission():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newLaunch = SpaceXLaunchManifest(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newLaunch)
        flash('New Launch %s Successfully Created' % newLaunch.name)
        session.commit()
        return redirect(url_for('showManifest'))
    else:
        return render_template('newmission.html')

# Edit a launch on the manifest
@app.route('/launch_manifest/<int:manifest_id>/edit/', methods=['GET', 'POST'])
def editMission(manifest_id):
    editedMission = session.query(
        SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    creator = getUserInfo(editedMission.user_id)
    if 'username' not in login_session:
        return redirect('/login')
    if editedMission.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this Mission. Please create your own Mission in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedMission.name = request.form['name']
            flash('Mission Successfully Edited %s' % editedMission.name)
            return redirect(url_for('showManifest'))
    else:
        return render_template('editMission.html', manifest=editedMission, creator=creator)


# Delete a launch on the manifest
@app.route('/launch_manifest/<int:manifest_id>/delete/', methods=['GET', 'POST'])
def deleteMission(manifest_id):
    missionToDelete = session.query(
        SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    creator = getUserInfo(missionToDelete.user_id)
    if 'username' not in login_session:
        return redirect('/login')
    if missionToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this Launch. Please create your own Launch in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(missionToDelete)
        flash('%s Successfully Deleted' % missionToDelete.name)
        session.commit()
        return redirect(url_for('showManifest', manifest_id=manifest_id))
    else:
        return render_template('deleteMission.html', mission=missionToDelete, creator=creator)

# Show a launch's details
@app.route('/launch_manifest/<int:manifest_id>/')
@app.route('/launch_manifest/<int:manifest_id>/launch/')
def showLaunch(manifest_id):
    manifest = session.query(SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    creator = getUserInfo(manifest.user_id)
    launch = session.query(Launches).filter_by(
        launch_id=manifest_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publiclaunches.html', manifest=manifest, launch=launch, creator=creator)
    else:
        return render_template('launches.html', manifest=manifest, launch=launch, creator=creator)


# Create a launch
@app.route('/launch_manifest/<int:manifest_id>/launch/new/', methods=['GET', 'POST'])
def newLaunch(manifest_id):
    if 'username' not in login_session:
        return redirect('/login')
    manifest = session.query(SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    if login_session['user_id'] != manifest.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add launches to this mission. Please create your own mission to add launches.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
            newLaunch = Launches(customer=request.form['customer'], 
                                description=request.form['description'], 
                                launch_date=request.form['launch_date'],
                                rocket_type=request.form['rocket_type'],  
                                launch_id=manifest_id, 
                                user_id=manifest.user_id)
            session.add(newLaunch)
            session.commit()
            flash('New Launch %s Successfully Created' % (newLaunch.customer))
            return redirect(url_for('showLaunch', manifest_id=manifest_id))
    else:
        return render_template('newlaunch.html', manifest_id=manifest_id)

# Edit a launch
@app.route('/launch_manifest/<int:manifest_id>/launch/<int:launch_id>/edit', methods=['GET', 'POST'])
def editLaunch(manifest_id, launch_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedLaunch = session.query(Launches).filter_by(id=launch_id).one()
    mission = session.query(SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    if login_session['user_id'] != mission.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit launches for this mission. Please create your own mission in order to edit launches.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['customer']:
            editedLaunch.name = request.form['customer']
        if request.form['description']:
            editedLaunch.description = request.form['description']
        if request.form['launch_date']:
            editedLaunch.launch_date = request.form['launch_date']
        if request.form['rocket_type']:
            editedLaunch.rocket_type = request.form['rocket_type']
        session.add(editedLaunch)
        session.commit()
        flash('Launch Successfully Edited')
        return redirect(url_for('showLaunch', manifest_id=manifest_id))
    else:
        return render_template('editlaunch.html', manifest_id=manifest_id, launch_id=launch_id, launch=editedLaunch)


# Delete a launch
@app.route('/launch_manifest/<int:manifest_id>/launch/<int:launch_id>/delete', methods=['GET', 'POST'])
def deleteLaunch(manifest_id, launch_id):
    if 'username' not in login_session:
        return redirect('/login')
    mission = session.query(SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    creator = getUserInfo(mission.user_id)
    launchToDelete = session.query(Launches).filter_by(id=launch_id).one()
    mission = session.query(SpaceXLaunchManifest).filter_by(id=manifest_id).one()
    if login_session['user_id'] != mission.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete launches from this mission. Please create your own mission in order to delete items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(launchToDelete)
        session.commit()
        flash('Launch %s Successfully Deleted' % (launchToDelete.customer))
        return redirect(url_for('showLaunch', manifest_id=manifest_id))
    else:
        return render_template('deletelaunch.html', launch=launchToDelete, creator=creator, mission=mission, manifest_id=manifest_id)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showManifest'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showManifest'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)