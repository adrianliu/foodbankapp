from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from todo import app
from todo import Db as db
from models import Task
import json

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

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
