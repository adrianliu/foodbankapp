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


