import os
import json
import sqlite3
from models import Request, Request_Detail, User

# From: https://goo.gl/YzypOI
def singleton(cls):
  instances = {}
  def getinstance():
    if cls not in instances:
      instances[cls] = cls()
    return instances[cls]
  return getinstance

class DB(object):
  """
  DB driver for the Todo app - deals with writing entities
  to the DB and reading entities from the DB
  """

  def __init__(self):
    self.conn = sqlite3.connect("todo.db", check_same_thread=False)
    # TODO - Create all other tables here
    self.create_user_table()
    self.create_request_table()
    self.create_event_detail_table()
    self.create_food_item_table()
    self.create_category_table()

  def create_task_table(self):
    """
    Create a Task table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE task
        (ID TEXT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        DESCRIPTION TEXT NOT NULL,
        TAGS TEXT NOT NULL,
        DUE_DATE INT NOT NULL,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def delete_task_table(self):
    # TODO - Implement this to delete a task table
    self.conn.execute("""
      DROP TABLE task;
      """)
    self.conn.commit()

  def create_task(self, task):
    """
    VALUES (task.id, task.name, task.description, task.tags, task.due_date);
    Insert a task to task table.
    """
    if not isinstance(task, Task):
      return
    self.conn.execute("""
      INSERT INTO task (ID,NAME,DESCRIPTION,TAGS,DUE_DATE)
      VALUES (?,?,?,?,?)""", (task.id, task.name, task.description, task.tags, task.due_date))
    self.conn.commit()

  def delete_task(self, task_id):
    """
    Delete the specific task from task table.
    """
    self.conn.execute("""
      DELETE from task where ID= (?)""",(task_id,))
    self.conn.commit()

  def delete_all_tasks(self):
    """
    Delete all tasks from task table.
    """
    self.conn.execute("""
      DELETE from task;
      """)
    self.conn.commit()

  def query_all_tasks(self):
    """
    Query tasks from Task table.
    """
    cursor = self.conn.execute("""
      SELECT * FROM task;
    """)

    tasks = []
    for row in cursor:
      id = row[0]
      name = row[1]
      description = row[2]
      tags = row[3]
      due_date = row[4]
      task = Task(name, description, tags, due_date, id)
      tasks.append(task.to_dict())
    return tasks

  def create_user_table(self):
    """
    Create a User table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE user
        (USERNAME TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL,
        NAME TEXT,
        ADDRESS TEXT,
        ZIP_CODE TEXT,
        CITY TEXT,
        STATE TEXT,
        COUNTRY TEXT,
        PHONE TEXT,
        EMAIL TEXT,
        DESCRIPTION TEXT,
        ORGANIZATION_TYPE TEXT,
        USER_TYPE TEXT,
        PICK_UP_METHOD TEXT,
        POPULATION TEXT,
        TOTAL_CAPACITY TEXT,
        CURRENT_INVENTORY TEXT,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def create_user(self, user):
    if not isinstance(user, User):
      return

    cursor = self.conn.execute("""
      SELECT username FROM user;
    """)
    for row in cursor:
      one_username = row[0]
      if str(one_username) == str(user.username):
        return False

    self.conn.execute("""
      INSERT INTO user (USERNAME,PASSWORD,NAME,ADDRESS,ZIP_CODE,CITY,STATE,COUNTRY,PHONE,EMAIL,DESCRIPTION,ORGANIZATION_TYPE,USER_TYPE,PICK_UP_METHOD,POPULATION,TOTAL_CAPACITY,CURRENT_INVENTORY)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (user.username, user.password, user.name, user.address, user.zip_code, user.city, user.state, user.country, user.phone, user.email, user.description, user.organization_type, user.user_type, user.pick_up_method, user.population, user.total_capacity, user.current_inventory))
    self.conn.commit()
    return True

  def user_login(self, username, password):
    cursor = self.conn.execute("""
      SELECT username, password FROM user;
    """)

    for row in cursor:
      one_username = row[0]
      one_password = row[1]
      if str(one_username) == str(username) and str(one_password) == str(password):
        return True
    return False

  def create_request_table(self):
    """
    Create a Request table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE request
        (REQUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FROM_USER TEXT,
        TO_USER TEXT,
        APPOINTMENT_DATE TEXT,
        APPOINTMENT_TIME TEXT,
        REQUEST_TYPE TEXT,
        BENEFICIARY TEXT,
        FREQUENCY TEXT,
        DESCRIPTION TEXT,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def create_request_header(self, request):
    if not isinstance(request, Request):
      return

    self.conn.execute("""
      INSERT INTO request (FROM_USER,TO_USER,APPOINTMENT_DATE,APPOINTMENT_TIME,REQUEST_TYPE,BENEFICIARY,FREQUENCY,DESCRIPTION)
      VALUES (?,?,?,?,?,?,?,?)""", (request.from_user, request.to_user, request.appointment_date, request.appointment_time, request.request_type, request.beneficiary, request.frequency, request.description))
    self.conn.commit()

  def create_request_detail_table(self):
    """
    Create a Request Detail table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE request_detail
        (REQUEST_DETAIL_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        REQUEST_HEADER_ID INTEGER NOT NULL,
        FOOD_ITEM_ID TEXT,
        QUANTITY TEXT,
        WEIGHT TEXT,
        EXPIRY_DATE TEXT,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def create_request_detail_entry(self, detail):
    if not isinstance(detail, Request_Detail):
      return

    self.conn.execute("""
      INSERT INTO request_detail (REQUEST_HEADER_ID,FOOD_ITEM_ID,QUANTITY,WEIGHT,EXPIRY_DATE)
      VALUES (?,?,?,?,?)""", (detail.request_header_id, detail.food_item_id, detail.quantity, detail.weight, detail.expiry_date))
    self.conn.commit()

  def create_food_item_table(self):
    """
    Create a Food Item table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE food_item
        (FOOD_ITEM_ID TEXT PRIMARY KEY NOT NULL,
        CATEGORY_ID TEXT,
        NAME TEXT,
        DESCRIPTION TEXT,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def create_category_table(self):
    """
    Create a Category table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE category
        (CATEGORY_ID TEXT PRIMARY KEY NOT NULL,
        CATEGORY_NAME TEXT,
        DESCRIPTION TEXT,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e


# Only <=1 instance of the DB driver
# exists within the app at all times
DB = singleton(DB)
