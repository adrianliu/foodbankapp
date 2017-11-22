import os
import json
import sqlite3
from models import Request, Request_Detail, User
from todo import constants as constants

def singleton(cls):
  instances = {}
  def getinstance():
    if cls not in instances:
      instances[cls] = cls()
    return instances[cls]
  return getinstance

class DB(object):
  """
  DB driver for the Food Bank app - deals with writing entities
  to the DB and reading entities from the DB
  """

  def __init__(self):
    self.conn = sqlite3.connect("todo.db", check_same_thread=False)
    # TODO - Create all other tables here
    self.create_user_table()
    self.create_request_table()
    self.create_request_detail_table()
    self.create_transaction_table()
    self.create_transaction_detail_table()
    self.create_food_item_table()
    self.create_category_table()

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
        USER_TYPE INTEGER,
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
      SELECT * FROM user;
    """)

    for row in cursor:
      one_username = row[0]
      one_password = row[1]
      if str(one_username) == str(username) and str(one_password) == str(password):
        name = row[2]
        user_type = row[12]
        new_user = User(one_username, one_password, name, None, None, None, None, None, None, None, None, None, user_type, None, None, None, None)
        return new_user
    return None

  def foodbank_query(self):
    cursor = self.conn.execute("""
      SELECT username FROM user where user_type = 0;
    """)

    foodbanks_username = []
    for row in cursor:
      one_foodbank_username = row[0]
      foodbanks_username.append(one_foodbank_username)
    return foodbanks_username

  def create_request_table(self):
    """
    Create a Request table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE request
        (REQUEST_ID TEXT PRIMARY KEY NOT NULL,
        FROM_USER TEXT,
        TO_USER TEXT,
        APPOINTMENT_DATE TEXT,
        APPOINTMENT_TIME TEXT,
        REQUEST_TYPE INTEGER,
        BENEFICIARY TEXT,
        FREQUENCY TEXT,
        DESCRIPTION TEXT,
        STATUS INTEGER NOT NULL,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def create_transaction_table(self):
    """
    Create a Transaction table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE transaction_header
        (TRANSACTION_ID TEXT PRIMARY KEY NOT NULL,
        FROM_USER TEXT,
        TO_USER TEXT,
        APPOINTMENT_DATE TEXT,
        APPOINTMENT_TIME TEXT,
        TRANSACTION_TYPE INTEGER,
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
      INSERT INTO request (REQUEST_ID,FROM_USER,TO_USER,APPOINTMENT_DATE,APPOINTMENT_TIME,REQUEST_TYPE,BENEFICIARY,FREQUENCY,DESCRIPTION,STATUS)
      VALUES (?,?,?,?,?,?,?,?,?,?)""", (request.request_id, request.from_user, request.to_user, request.appointment_date, request.appointment_time, request.request_type, request.beneficiary, request.frequency, request.description, request.status))
    self.conn.commit()
    return request.request_id

  def create_transaction_header(self, transaction):
    if not isinstance(transaction, Transaction):
      return

    self.conn.execute("""
      INSERT INTO transaction_header (TRANSACTION_ID,FROM_USER,TO_USER,APPOINTMENT_DATE,APPOINTMENT_TIME,TRANSACTION_TYPE,BENEFICIARY,FREQUENCY,DESCRIPTION)
      VALUES (?,?,?,?,?,?,?,?,?)""", (transaction.transaction_id, transaction.from_user, transaction.to_user, transaction.appointment_date, transaction.appointment_time, transaction.transaction_type, transaction.beneficiary, transaction.frequency, transaction.description))
    self.conn.commit()
    return transaction.transaction_id

  def create_request_detail_table(self):
    """
    Create a Request Detail table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE request_detail
        (REQUEST_DETAIL_ID TEXT PRIMARY KEY NOT NULL,
        REQUEST_HEADER_ID TEXT NOT NULL,
        FOOD_ITEM_ID INTEGER,
        CATEGORY_ID INTEGER,
        QUANTITY TEXT,
        WEIGHT TEXT,
        EXPIRY_DATE TEXT,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def create_transaction_detail_table(self):
    """
    Create a Transaction Detail table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE transaction_detail
        (TRANSACTION_DETAIL_ID TEXT PRIMARY KEY NOT NULL,
        TRANSACTION_HEADER_ID TEXT NOT NULL,
        FOOD_ITEM_ID INTEGER,
        CATEGORY_ID INTEGER,
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
      INSERT INTO request_detail (REQUEST_DETAIL_ID,REQUEST_HEADER_ID,FOOD_ITEM_ID,CATEGORY_ID,QUANTITY,WEIGHT,EXPIRY_DATE)
      VALUES (?,?,?,?,?,?,?)""", (detail.request_detail_id, detail.request_header_id, detail.food_item_id, detail.category_id, detail.quantity, detail.weight, detail.expiry_date))
    self.conn.commit()

  def create_transaction_detail_entry(self, detail):
    if not isinstance(detail, Transaction_Detail):
      return

    self.conn.execute("""
      INSERT INTO transaction_detail (TRANSACTION_DETAIL_ID,TRANSACTION_HEADER_ID,FOOD_ITEM_ID,CATEGORY_ID,QUANTITY,WEIGHT,EXPIRY_DATE)
      VALUES (?,?,?,?,?,?,?)""", (detail.transaction_detail_id, detail.transaction_header_id, detail.food_item_id, detail.category_id, detail.quantity, detail.weight, detail.expiry_date))
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

    self.conn.execute("""
      DELETE FROM category;""")
    self.conn.commit()

    self.create_category_entry("1", "Vegetables", "shucai")
    self.create_category_entry("2", "Fruit", "shuiguo")
    self.create_category_entry("3", "Grain", "guwu")
    self.create_category_entry("4", "Meat", "rou")
    self.create_category_entry("5", "Milk", "nai")

  def create_category_entry(self, category_id, category_name, description):
    self.conn.execute("""
      INSERT INTO category (CATEGORY_ID, CATEGORY_NAME,DESCRIPTION)
      VALUES (?,?,?)""", (category_id, category_name, description))
    self.conn.commit()

  def category_query(self):
    cursor = self.conn.execute("""
      SELECT category_id, category_name FROM category;
    """)

    categories = {}
    for row in cursor:
      categories[row[0]] = row[1]
    return categories

  def fetch_request(self, username):
    cursor = self.conn.execute("""
      SELECT * FROM request where status == 0 AND to_user = (?)""",(username,))

    donations = []
    consumptions = []
    for row in cursor:
      request_id = row[0]
      from_user = row[1]
      # to_user = row[2]
      appointment_date = row[3]
      appointment_time = row[4]
      request_type = row[5]
      beneficiary = row[6]
      frequency = row[7]
      description = row[8]
      status = row[9]
      create_date = row[10]

      new_request = Request(from_user, username, appointment_date, appointment_time, request_type, beneficiary, frequency, description, status, create_date, request_id)
      if request_type == constants.REQUEST_DONATION:
        donations.append(new_request)
      else:
        consumptions.append(new_request)
    return donations, consumptions

  def update_request(self, request_id):
    cursor = self.conn.execute("""
      UPDATE request SET status = 1 where request_id = (?)""",(request_id,))

  def approve_request(self, request_id):
    self.conn.execute("""
      UPDATE request SET status = 1 where request_id = (?)""",(request_id,))
    self.conn.commit()

  def fetch_one_whole_request(self, request_id):
    cursor = self.conn.execute("""
      SELECT * FROM request where request_id = (?)""",(request_id,))
    request_header = []
    for row in cursor:
      # request_id = row[0]
      from_user = row[1]
      to_user = row[2]
      appointment_date = row[3]
      appointment_time = row[4]
      request_type = row[5]
      beneficiary = row[6]
      frequency = row[7]
      description = row[8]
      status = row[9]
      create_date = row[10]
      new_request = Request(from_user, to_user, appointment_date, appointment_time, request_type, beneficiary, frequency, description, status, create_date, request_id)
      request_header.append(new_request)

    cursor = self.conn.execute("""
      SELECT * FROM request_detail where request_header_id = (?)""",(request_id,)) 
    request_detail = []
    for row in cursor:
      request_detail_id = row[0]
      # request_header_id = row[1]
      food_item_id = row[2]
      category_id = row[3]
      quantity = row[4]
      weight = row[5]
      expiry_date = row[6]
      new_request_detail = Request_Detail(request_id, food_item_id, category_id, quantity, weight, expiry_date, request_detail_id)
      request_detail.append(new_request_detail)
    return request_header, request_detail


# Only <=1 instance of the DB driver
# exists within the app at all times
DB = singleton(DB)
