from google.appengine.ext import ndb

class Spoogler(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    spoogler_email = ndb.StringProperty()
    googler_email = ndb.StringProperty()
    status = ndb.StringProperty() # 'Inactive' or 'Active'
    token = ndb.IntegerProperty()
