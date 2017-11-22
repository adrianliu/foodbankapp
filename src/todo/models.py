from abc import ABCMeta
import uuid
import json

class Model(object):
  """
  Abstract base class for all models -
  all models should extend this class
  """
  __metaclass__ = ABCMeta

  def __init__(self, id):
    """
    Initializes the model with a Universal Unique
    Identifier as an id
    """
    if id == None:
      self.id = str(uuid.uuid1())
    else:
      self.id = id

  def to_dict(self):
    """
    Dictionary representation of this Model
    """
    return vars(self)


class Task(Model):
  """
  class for all Task model
  """
  def __init__(self, name, description, tags, due_date, id = None):
    if id == None:
      self.id = str(uuid.uuid1())
    else:
      self.id = id
    self.name = name #string
    self.description = description # string
    self.tags = tags # string with comma
    self.due_date = due_date # int, total seconds in unix time

  def to_dict(self):
    return super(Task, self).to_dict()

class User(Model):
  def __init__(self, username, password, name, address, zip_code, city, state, country, phone, email, description, organization_type, user_type, pick_up_method, population, total_capacity, current_inventory):
    self.username = username
    self.password = password
    self.name = name
    self.address = address
    self.zip_code = zip_code
    self.city = city
    self.state = state
    self.country = country
    self.phone = phone
    self.email = email
    self.description = description
    self.organization_type = organization_type
    self.user_type = user_type
    self.pick_up_method = pick_up_method
    self.population = population
    self.total_capacity = total_capacity
    self.current_inventory = current_inventory

class Request(Model):
  def __init__(self, from_user, to_user, appointment_date, appointment_time, request_type, beneficiary, frequency, description, status, create_date = None, request_id = None):
    if request_id == None:
      self.request_id = str(uuid.uuid1())
    else:
      self.request_id = request_id
    self.from_user = from_user
    self.to_user = to_user
    self.appointment_date = appointment_date
    self.appointment_time = appointment_time
    self.request_type = request_type
    self.beneficiary = beneficiary
    self.frequency = frequency
    self.description = description
    self.status = status
    self.create_date = create_date
    
class Request_Detail(Model):
  def __init__(self, request_header_id, food_item_id, category_id, quantity, weight, expiry_date, request_detail_id = None):
    if request_detail_id == None:
      self.request_detail_id = str(uuid.uuid1())
    else:
      self.request_detail_id = request_detail_id
    self.request_header_id = request_header_id
    self.food_item_id = food_item_id
    self.category_id = category_id
    self.quantity = quantity
    self.weight = weight
    self.expiry_date = expiry_date

class Transaction(object):
  def __init__(self, from_user, to_user, appointment_date, appointment_time, transaction_type, beneficiary, frequency, description, create_date = None, transaction_id = None):
    if transaction_id == None:
      self.transaction_id = str(uuid.uuid1())
    else:
      self.transaction_id = transaction_id
    self.from_user = from_user
    self.to_user = to_user
    self.appointment_date = appointment_date
    self.appointment_time = appointment_time
    self.transaction_type = transaction_type
    self.beneficiary = beneficiary
    self.frequency = frequency
    self.description = description
    self.create_date = create_date

class Transaction_Detail(Model):
  def __init__(self, transaction_header_id, food_item_id, category_id, quantity, weight, expiry_date, transaction_detail_id = None):
    if transaction_detail_id == None:
      self.transaction_detail_id = str(uuid.uuid1())
    else:
      self.transaction_detail_id = transaction_detail_id
    self.transaction_header_id = transaction_header_id
    self.food_item_id = food_item_id
    self.category_id = category_id
    self.quantity = quantity
    self.weight = weight
    self.expiry_date = expiry_date
