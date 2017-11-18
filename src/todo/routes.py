from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from todo import app
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
		if db.user_login(username, password):
			session['logged_in'] = True
			session['username'] = username
			return redirect(url_for('login_donor'))
		else:
			# todo
			return "Incorrect username or password"

@app.route('/login/donor/', methods=['GET', 'POST'])
def login_donor():
	if session['logged_in']:
		return render_template('login_donor.html')	
	else:
		flash('wrong password!')

@app.route('/donate', methods=['GET', 'POST'])
def donate_request():
	if session['logged_in']:
		return render_template('donate_request.html')
	else:
		flash('wrong password!')

@app.route('/submit/donate', methods=['GET', 'POST'])
def submit_donate_request():
	if session['logged_in'] and request.method == 'POST':
		from_user = session['username']
		to_user = request.form['to_user']
		appointment_date = request.form['date']
		appointment_time = request.form['time']		
		request_type = 1
		beneficiary = request.form['beneficiary']
		frequency = request.form['frequency']
		description = request.form['description']

		food_item_id = request.form['food_item_id']
		quantity = request.form['quantity']
		weight = request.form['weight']
		expiry_date = request.form['expiry_date']

		new_request = Request(from_user, to_user, appointment_date, appointment_time, request_type, beneficiary, frequency, description)
		db.create_request_header(new_request)
		return "succeed"

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
		name = None;
		address = None;
		zip_code = None;
		city = None;
		state = None;
		country = None;
		phone = None;
		email = None;
		description = None;
		organization_type = None;
		user_type = None;
		pick_up_method = None;
		population = None;
		total_capacity = None;
		current_inventory = None;
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
