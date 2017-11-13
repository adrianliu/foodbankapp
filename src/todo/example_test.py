from abc import ABCMeta
import uuid
from datetime import datetime

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
  def __init__(self, name, discription, tags, due_date, id = None):
    super(Task, self).__init__(id) #Model.__init__(self, id)
    self.name = name #string
    self.discription = discription # string
    self.tags = tags # string with comma
    self.due_date = due_date # int, total seconds in unix time
    self.created_at = int((datetime.now()-datetime(1970,1,1)).total_seconds())

  def to_dict(self):
    return super(Task, self).to_dict()

task1 = Task("jogging", "need to jogging", "run, jogging, exercise", 1999)
print task1.to_dict()
task2 = Task("jogging", "need to jogging", "run, jogging, exercise", 1999, "new id")
print task2.to_dict()
