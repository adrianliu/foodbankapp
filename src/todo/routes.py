from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from todo import app
from todo import constants as constants
from todo import Db as db
from models import Request, Request_Detail, User
import json

@app.route('/')
def main_menu():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_complete():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = db.user_login(username, password)
		if user == None:
			# todo
			return "Incorrect username or password"			
		else:
			user_type = user.user_type
			session['username'] = username
			session['user_type'] = user_type
			if user_type == constants.TYPE_DONOR:
				return redirect(url_for('login_donor'))
			elif user_type == constants.TYPR_CONSUMER:
				return redirect(url_for('login_consumer'))
			elif user_type == constants.TYPE_FOODBANK:
				return redirect(url_for('login_foodbank'))

@app.route('/login/donor/', methods=['GET', 'POST'])
def login_donor():
	if session['logged_in']:
		return render_template('login_donor.html')

@app.route('/login/consumer/', methods=['GET', 'POST'])
def login_consumer():
	if session['logged_in']:
		return render_template('login_consumer.html')

@app.route('/login/foodbank/', methods=['GET', 'POST'])
def login_foodbank():
	if session['logged_in']:
		donations, consumptions = db.fetch_request(session['username'])		
		return render_template('login_foodbank.html', donations = donations, consumptions = consumptions)

@app.route('/request/donate', methods=['GET', 'POST'])
def request_donate():
	if session['logged_in']:
		foodbanks_username = db.foodbank_query()
		categories = db.category_query()
		print categories
		return render_template('request_donate.html', foodbanks_username = foodbanks_username, categories = categories)

@app.route('/submit/donate', methods=['GET', 'POST'])
def submit_donate_request():
	if session['logged_in'] and request.method == 'POST':
		from_user = session['username']
		to_user = request.form['to_user']
		appointment_date = request.form['date']
		appointment_time = request.form['time']		
		request_type = constants.REQUEST_DONATION
		beneficiary = request.form['beneficiary']
		frequency = request.form['frequency']
		description = request.form['description']

		food_item_id = request.form['food_item_id']
		category_id = request.form['category_id']
		quantity = request.form['quantity']
		weight = request.form['weight']
		expiry_date = request.form['expiry_date']

		new_request = Request(from_user, to_user, appointment_date, appointment_time, request_type, beneficiary, frequency, description, constants.REQUEST_PENDING)
		request_id = db.create_request_header(new_request)
		new_request_detail = Request_Detail(request_id, food_item_id, category_id, quantity, weight, expiry_date)
		db.create_request_detail_entry(new_request_detail)
		return "succeed"

@app.route('/request/claim', methods=['GET', 'POST'])
def request_claim():
	if session['logged_in']:
		return render_template('request_claim.html')

@app.route('/request/edit', methods=['GET', 'POST'])
def request_edit():
	if session['logged_in']:
		request_id = request.form['request_id']
		request_header, request_detail = db.fetch_one_whole_request(request_id)
		if len(request_header) == 0 or len(request_detail) == 0:
			return "error"
		else:
			return render_template('request_edit.html', request_header = request_header[0], request_detail = request_detail)

@app.route('/transaction/add', methods=['GET', 'POST'])
def transaction_add():
	if session['logged_in']:
		if request.form['submit'] == 'save':
			return "save"
		elif request.form['submit'] == 'approve':
			db.approve_request(request.form['request_id'])
			return "approve"
		else:
			return redirect(url_for('login_foodbank'))

@app.route('/signup/donor', methods=['GET', 'POST'])
def signup_donor():
	return render_template('signup_donor.html')

@app.route('/signup/consumer', methods=['GET', 'POST'])
def signup_consumer():
	return render_template('signup_consumer.html')

@app.route('/signup/foodbank', methods=['GET', 'POST'])
def signup_foodbank():
	return render_template('signup_foodbank.html')

@app.route('/signup/complete', methods=['GET', 'POST'])
def signup_complete():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		name = None
		address = None
		zip_code = None
		city = None
		state = None
		country = None
		phone = None
		email = None
		description = None
		organization_type = None
		user_type = request.form['user_type']
		pick_up_method = None
		population = None
		total_capacity = None
		current_inventory = None
		new_user = User(username, password, name, address, zip_code, city, state, country, phone, email, description, organization_type, user_type, pick_up_method, population, total_capacity, current_inventory)
		if db.create_user(new_user):
			return "Sign Up Complete!"
		else:
			return "Username already exists!"

# @app.route('/')
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return "Hello Boss!"
 
# @app.route('/login', methods=['POST'])
# def do_admin_login():
#     if request.form['password'] == 'password' and request.form['username'] == 'admin':
#         session['logged_in'] = True
#     else:
#         flash('wrong password!')
#     return home()

# @app.route('/tasks', methods=['GET', 'POST'])
# def get_tasks():
# 	if request.method == 'POST':
# 		name = request.json['name']
# 		description = request.json['description']
# 		tags = request.json['tags']
# 		due_date = int(request.json['due_date'])
# 		new_task = Task(name, description, tags, due_date)
# 		db.create_task(new_task)
# 		#If POST request, then send back the new created task to user
# 		return jsonify(new_task.to_dict())
# 	else:
# 		#If GET request, then send back all of the tasks from database to user
# 		tasks = db.query_all_tasks()
# 		return json.dumps(tasks)

# @app.route('/tasks', methods=['DELETE'])
# def delete_task():
# 	task_id = request.form['id']
# 	db.delete_task(task_id)
# 	return jsonify({ 'success': 'true' })

# @app.route('/tasks/all', methods=['DELETE'])
# def delete_all_tasks():
# 	db.delete_all_tasks()
# 	return jsonify({ 'success': 'true' })
