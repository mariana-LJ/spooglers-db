from google.appengine.ext import ndb

class Spoogler(ndb.Model):
  firstName = ndb.StringProperty()
  lastName = ndb.StringProperty()
  email = ndb.StringProperty()
  googlerEmail = ndb.StringProperty()
  status = ndb.StringProperty() # 'Inactive' or 'Active'
  token = ndb.IntegerProperty()
