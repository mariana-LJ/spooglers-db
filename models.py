from google.appengine.ext import ndb

# Spoogler's current work status
work_status = [
    (0, "Visa allows work"),
    (1, "Visa does not allow work"),
    (2, "Able to work"),
    (3, "Not able to work")]

# Spoogler's English language proficiency
english_proficiency = [
    (0, "Fully fluent/native speaker"),
    (1, "Almost fluent"),
    (2, "Conversational"),
    (3, "Minimal"),
    (4, "None")]

# Spoogler's address in the Bay Area
address_options = [
    (0, "East Bay"),
    (1, "South Bay"),
    (2, "Peninsula"),
    (3, "San Francisco"),
    (4, "North Bay"),
    (5, "Other")]

# Time living in the Bay Area
time = [
    (0, "6 months or less"),
    (1, "Less than 1 year"),
    (2, "More than 1 year")]

# Mode of transportation
transportation = [
    (0, "Driving personal/family car"),
    (1, "Carpooling"),
    (2, "Public transit"),
    (3, "Bicycle"),
    (4, "Walking")]

# Side of the road to drive
side_driving = [
    (0, "left"),
    (1, "right")]

# Size of events to attend
event_size = [
    (0, "Small, informal local groups (i.e. coffee at local cafe)"),
    (1, "Large groups (i.e. family picnics)"),
    (2, "Large regional get-togethers and parties for special occasions")]

# Type of events to attend
event_type = [
    (0, "Arts and crafts"),
    (1, "Beauty/personal grooming"),
    (2, "Book club"),
    (3, "Career counseling (for those who cannot work)"),
    (4, "Casual mid-morning coffee"),
    (5, "Concerts, theater"),
    (6, "Cooking"),
    (7, "Date nights, movies"),
    (8, "Dinner, drinks"),
    (9, "Education/skills sharing"),
    (10, "Family picnics"),
    (11, "Games, board games"),
    (12, "Playdates"),
    (13, "Sightseeing"),
    (14, "Sports"),
    (15, "Volunteering"),
    (16, "Other")]

# Type of support services Spoogler is looking for
support_type = [
    (0, "Local recommendations (i.e. for housing, health specialists, schools, etc.)"),
    (1, "Information (i.e. on US taxes, healthcare system, building credit, visas, etc.)"),
    (2, "Networking (based on home country, interests, current residence, etc.)"),
    (3, "Other")]

# Other types of support used by Spoogler
support_other = [
    (0, "Family/friends here"),
    (1, "Country of origin or ethnicity-based groups"),
    (2, "Faith-based groups"),
    (3, "Other")]

# Spoogler's children ages
children_ages = [
    (0, "No children"),
    (1, "Expecting"),
    (2, "Infant"),
    (3, "Preschool, kindergarten"),
    (4, "Elementary school"),
    (5, "Middle school"),
    (6, "High school"),
    (7, "College/university"),
    (8, "Left home")]


class Spoogler(ndb.Model):
    full_name = ndb.StringProperty()
    spoogler_email = ndb.StringProperty()
    spoogler_fb_email = ndb.StringProperty()
    googler_ldap = ndb.StringProperty()
    spoogler_country = ndb.StringProperty()
    work_status = ndb.IntegerProperty(repeated=None)  # See work_status list
    engl_proficiency = ndb.StringProperty()
    spoogler_lang2 = ndb.StringProperty()
    native_lang = ndb.StringProperty()
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
