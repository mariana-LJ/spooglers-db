from google.appengine.ext import ndb

class Spoogler(ndb.Model):
    full_name = ndb.StringProperty()
    spoogler_email = ndb.StringProperty()
    spoogler_fb_email = ndb.StringProperty()
    googler_ldap = ndb.StringProperty()
    spoogler_country = ndb.StringProperty()
    work_status = ndb.StringProperty()
    engl_proficiency = ndb.StringProperty()
    spoogler_lang2 = ndb.StringProperty()
    spoogler_lang = ndb.StringProperty()
    address = ndb.StringProperty()
    time = ndb.StringProperty()
    spoogler_relo = ndb.StringProperty()
    transportation = ndb.StringProperty()
    side_driving = ndb.StringProperty()
    spoogler_events_size = ndb.StringProperty()
    event_type = ndb.StringProperty()
    support_type = ndb.StringProperty()
    support_other = ndb.StringProperty()
    children_ages = ndb.StringProperty()
    status = ndb.StringProperty() # 'Inactive' or 'Active'
    token = ndb.IntegerProperty()
