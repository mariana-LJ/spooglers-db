from google.appengine.ext import ndb

# Spoogler's current work status
work_status_list = [
    (0, "Please select"),
    (1, "Visa allows work"),
    (2, "Visa does not allow work"),
    (3, "Able to work"),
    (4, "Not able to work")]

# Spoogler's English language proficiency
proficiency_list = [
    (0, "Please select"),
    (1, "Fully fluent/native speaker"),
    (2, "Almost fluent"),
    (3, "Conversational"),
    (4, "Minimal"),
    (5, "None")]

# Spoogler languages
languages_list = [
    ("None", "Please select"),
    ("English", "English"),
    ("Mandarin", "Mandarin"),
    ("Spanish", "Spanish"),
    ("Hindi", "Hindi"),
    ("French", "French"),
    ("Russian", "Russian"),
    ("German", "German")]

# Spoogler's address in the Bay Area
address_options_list = [
    (0, "Please select"),
    (1, "East Bay"),
    (2, "South Bay"),
    (3, "Peninsula"),
    (4, "San Francisco"),
    (5, "North Bay"),
    (6, "Other")]

# Time living in the Bay Area
times_list = [
    (0, "Please select"),
    (1, "6 months or less"),
    (2, "Less than 1 year"),
    (3, "More than 1 year")]

# Mode of transportation
transportation_list = [
    (0, "Please select"),
    (1, "Driving personal/family car"),
    (2, "Carpooling"),
    (3, "Public transit"),
    (4, "Bicycle"),
    (5, "Walking")]

# Side of the road to drive
side_driving_list = [
    (0, "Please select"),
    (1, "left"),
    (2, "right")]

# Size of events to attend
event_size_list = [
    (0, "Small, informal local groups (i.e. coffee at local cafe)"),
    (1, "Large groups (i.e. family picnics)"),
    (2, "Large regional get-togethers and parties for special occasions")]

# Type of events to attend
event_type_list = [
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
    (15, "Volunteering")]

# Type of support services Spoogler is looking for
support_type_list = [
    (0, "Local recommendations (i.e. for housing, health specialists, schools, etc.)"),
    (1, "Information (i.e. on US taxes, healthcare system, building credit, visas, etc.)"),
    (2, "Networking (based on home country, interests, current residence, etc.)")]

# Other types of support used by Spoogler
support_other_list = [
    (0, "Family/friends here"),
    (1, "Country of origin or ethnicity-based groups"),
    (2, "Faith-based groups")]

# Spoogler's children ages
children_ages_list = [
    (0, "Expecting"),
    (1, "Infant"),
    (2, "Preschool, kindergarten"),
    (3, "Elementary school"),
    (4, "Middle school"),
    (5, "High school"),
    (6, "College/university"),
    (7, "Left home")]


class Spoogler(ndb.Model):
    full_name = ndb.StringProperty()
    spoogler_email = ndb.StringProperty()
    spoogler_fb_email = ndb.StringProperty()
    googler_ldap = ndb.StringProperty()
    spoogler_country = ndb.StringProperty()
    work_status = ndb.IntegerProperty(repeated=False)  # See work_status_list
    languages = ndb.StringProperty(repeated=True) # See languages_list
    lang_proficiencies = ndb.IntegerProperty(repeated=True)  # See proficiency_list
    address = ndb.IntegerProperty(repeated=False)  # See address_options_list
    other_address = ndb.StringProperty(repeated=False)  # Spoogler address if option "Other" is selected
    time_in_area = ndb.IntegerProperty(repeated=False)  # See times_list
    spoogler_relo = ndb.StringProperty()
    transportation = ndb.IntegerProperty(repeated=False)  # See transportation_list
    side_driving = ndb.IntegerProperty(repeated=False)  # See side_driving_list
    events_size = ndb.IntegerProperty(repeated=True)  # See event_size_list
    event_types = ndb.IntegerProperty(repeated=True)  # See event_type_list
    event_types_other = ndb.StringProperty(repeated=False)  # Other event type suggested by Spoogler in the form
    support_types = ndb.IntegerProperty(repeated=True)  # See support_type_list
    support_types_other = ndb.StringProperty(repeated=False)  # Other type of support suggested by Spoogler
    support_others = ndb.IntegerProperty(repeated=True)  # See support_other_list
    support_others_other = ndb.StringProperty(repeated=False) # Other type of support accessed by Spoogler
    children_ages = ndb.IntegerProperty(repeated=True)  # See children_ages_list
    status = ndb.StringProperty() # 'Inactive' or 'Active'
    token = ndb.IntegerProperty()
