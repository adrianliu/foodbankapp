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
  """
  class for all Task model
  """
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

