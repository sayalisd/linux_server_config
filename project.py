from flask import Flask, render_template, url_for, request
from flask import redirect, flash, jsonify, json, make_response
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import jsonpickle


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())\
				['web']['client_id']
APPLICATION_NAME = "Catalog Application"

app = Flask(__name__)


# all functions for login/logout/create user/check user etc
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

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
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
        				connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print output
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
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCatalog'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Showing json for the catalog : http://localhost:8000/catalog.json
@app.route('/catalog.json')  # '/catalog/<catalog_name>/JSON')
def catalogJson():
	test_items = []
	test_dict = {}
	category = session.query(Category).all()
	for cat in category:
		items = session.query(CategoryItem).filter_by(category_id=cat.id).all()
		test_items.append([cat.serialize, ([i.serialize for i in items])])
		test_dict["Category"] = test_items
	return (jsonpickle.encode(test_dict, unpicklable=False, max_depth=5))


# Json for particular category: http://localhost:8000/catalog/Snowboarding/JSON
@app.route('/catalog/<category_name>/JSON')
def categoryJson(category_name):
	cat_data = session.query(Category).filter_by(name=
				category_name).one()
	citem_data = session.query(CategoryItem).filter_by(category_id=
				cat_data.id).all()

	return jsonify(Category=[cat_data.serialize], Items=[i.serialize
								for i in citem_data])


# Json for item: http://localhost:8000/catalog/Snowboarding/Snowboard/JSON
@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemJson(category_name, item_name):
	cat_data = session.query(Category).filter_by(name=category_name).one()
	citem_data = session.query(CategoryItem).filter_by(title=item_name).one()
	print citem_data.title
	return jsonify(Items=[citem_data.serialize])


# Showing all catalog : http://localhost:8000/
@app.route('/')
@app.route('/catalog/')
def showCatalog():
	catalog = session.query(Category).all()  # order_by(asc(Category.name))
	# show latest added items
	datalist = {}
	data = session.query(CategoryItem).order_by(CategoryItem.id.desc())\
					.limit(6).all()[::-1]
	for d in data:
		catitemname = d.title
		catitemid = d.id
		catid = d.category_id
		category = session.query(Category).filter_by(id=catid).one()
		# datalist[catitemid,catitemname] = category.name
		datalist[catitemname] = category.name
	if 'username' not in login_session:  # page without 'Add item' option
		return render_template('publiccatalog.html', catalog=catalog, data=datalist)
	else:
		return render_template('showcatalog.html', catalog=catalog, data=datalist)


# Showing items for category-http://localhost:8000/catalog/Snowboarding/items
@app.route('/catalog/<category_name>/items')
def showSpecificItems(category_name):
	catid = session.query(Category).filter_by(name=category_name).one()
	citem_data = session.query(CategoryItem).filter_by(category_id=catid.id).all()
	count = session.query(CategoryItem).filter_by(category_id=catid.id).count()
	return render_template('showcatitem.html', items=citem_data,
					category_name=category_name, count=count)


# Showing particular item: http://localhost:8000/catalog/Snowboarding/Snowboard
@app.route('/catalog/<category_name>/<categoryitem_name>')
def catalogItem(category_name, categoryitem_name):
	cat_data = session.query(Category).filter_by(name=category_name).one()
	citem_data = session.query(CategoryItem).\
			filter_by(title=categoryitem_name).one()
	if 'username' not in login_session:  # page without 'Edit|Delete' option
		return render_template('publiccatitem.html', items=citem_data,
					category_name=category_name)
	else:
		return render_template('showitem.html', items=citem_data,
					category_name=category_name)


# Add category item: http://localhost:8000/catalog/new (logged in)
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
	catalog = session.query(Category).all()
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		category_name = request.form['category']
		catalog_data = session.query(Category).filter_by(name=category_name).one()
		newItem = CategoryItem(title=request.form['title'],
							description=request.form['description'],
							category_id=catalog_data.id,
							user_id=login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash("New item created")
		return redirect(url_for('showSpecificItems', category_name=category_name))
	else:
		return render_template('newitem.html', categories=catalog)


# Edit catalog item : http://localhost:8000/catalog/Snowboard/edit (logged in)
@app.route('/catalog/<categoryitem_name>/edit/', methods=['GET', 'POST'])
def editCategory(categoryitem_name):
	categories = session.query(Category).all()
	cid = session.query(CategoryItem).filter_by(title=categoryitem_name).one()
	editCat = session.query(CategoryItem).filter_by(id=cid.id).one()
	category_id = editCat.category_id
	categorydata = session.query(Category).filter_by(id=category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editCat.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized\
		to edit this item. Please create your own item in order\
		to edit.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['title']:
			editCat.title = request.form['title']
		if request.form['description']:
			editCat.description = request.form['description']
		if request.form['category']:
			category = request.form['category']
			catdata = session.query(Category).filter_by(name=category).one()
			editCat.category_id = catdata.id
		session.add(editCat)
		session.commit()
		flash("Catalog item edited")
		return redirect(url_for('catalogItem', categoryitem_name=editCat.title,
							category_name=catdata.name))
	else:
		return render_template('edititem.html', categoryitem_name=categoryitem_name,
						item=editCat, categories=categories,
						category_name=categorydata.name)


# delete catalog item: http://localhost:8000/catalog/Snowboard/delete
@app.route('/catalog/<categoryitem_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(categoryitem_name):
	cid = session.query(CategoryItem).filter_by(title=categoryitem_name).one()
	deleteCat = session.query(CategoryItem).filter_by(id=cid.id).one()
	category_id = deleteCat.category_id
	categorydata = session.query(Category).filter_by(id=category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if deleteCat.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized\
		to delete this item. Please create your own item in order\
		to delete.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(deleteCat)
		session.commit()
		flash("Category item deleted")
		return redirect(url_for('showSpecificItems',
								category_name=categorydata.name))
	else:
		return render_template('deleteitem.html',
								categoryitem_name=categoryitem_name,
								catdata=categorydata)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)
