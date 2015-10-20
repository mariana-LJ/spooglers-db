from google.appengine.ext import ndb
from google.appengine.api import users

# List of ambassadors
ambassadors_list = [
    (0, "Webmaster", "bayareaspooglers.webmaster@gmail.com"),
    (1, "Bay Area Spooglers", "bayareaspooglers@gmail.com"),
    (2, "Puja Sharma", "puja.sharma159@gmail.com"),
    (3, "Sarah Ison", "ison.sarahj@gmail.com")]

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
    (0, "Please select"),
    (1, "English"),
    (2, "Spanish"),
    (3, "French"),
    (4, "Hindi"),
    (5, "German"),
    (6, "Mandarin"),
    (7, "Russian"),
    (8, "Italian"),
    (9, "Japanese"),
    (10, "Korean"),
    (11, "Other")]

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

# Spoogler's registration status
status_list = [
    (0, "Inactive"),
    (1, "Active"),]


class Spoogler(ndb.Model):
    full_name = ndb.StringProperty()
    spoogler_email = ndb.StringProperty()
    spoogler_fb_email = ndb.StringProperty()
    googler_full_name = ndb.StringProperty(repeated=False)
    googler_ldap = ndb.StringProperty()
    spoogler_country = ndb.StringProperty()
    work_status = ndb.IntegerProperty(repeated=False)  # See work_status_list
    english_proficiency = ndb.IntegerProperty(repeated=False) # See proficiency_list
    native_lang = ndb.IntegerProperty(repeated=False)  # See languages_list
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
    support_others_other = ndb.StringProperty(repeated=False)  # Other type of support accessed by Spoogler
    children_ages = ndb.IntegerProperty(repeated=True)  # See children_ages_list
    status = ndb.IntegerProperty(repeated=False)  # See status_list
    token = ndb.IntegerProperty()
    date_created = ndb.DateProperty(auto_now_add=True)
    on_google_group = ndb.BooleanProperty(default=False)
    on_google_group_date = ndb.DateProperty(auto_now=True)  # The date changes when there is an update
    on_facebook = ndb.BooleanProperty(default=False)
    on_facebook_date = ndb.DateProperty(auto_now=True)  # The date changes when there is an update
    on_fb_kids = ndb.BooleanProperty(default=False)
    on_fb_kids_date = ndb.DateProperty(auto_now=True)  # The date changes when there is an update
    ambassador = ndb.StringProperty(repeated=False)  # See ambasadors_list
    migrated = ndb.BooleanProperty(default=False)
    test = ndb.BooleanProperty(default=False)


def init_multiple_options(template_context):
    """Initializes the template fields that contains multiple options
    in the form."""
    template_context['work_status_list'] = work_status_list
    template_context['languages_list'] = languages_list
    template_context['proficiency_list'] = proficiency_list
    template_context['address_list'] = address_options_list
    template_context['times_list'] = times_list
    template_context['transportation_list'] = transportation_list
    template_context['side_driving_list'] = side_driving_list
    template_context['event_size_list'] = event_size_list
    template_context['event_type_list'] = event_type_list
    template_context['support_type_list'] = support_type_list
    template_context['support_other_list'] = support_other_list
    template_context['children_ages_list'] = children_ages_list
    template_context['status_list'] = status_list


def get_spoogler_context(request, template_context):
    """ Read the information from the form to build the context.
    :param template_context
    :return:
    """
    user = users.get_current_user()
    logout_url = users.create_logout_url(request.path)
    template_context.update({
        'full_name': request.get('full_name').strip(),
        'spoogler_email': request.get('spoogler_email').strip(),
        'spoogler_fb_email': request.get('spoogler_fb_email').strip(),
        'googler_full_name': request.get('googler_full_name').strip(),
        'googler_ldap': request.get('googler_ldap').strip(),
        'spoogler_country': request.get('spoogler_country').strip(),
        'work_status': int(request.get('work_status', '0').strip()),
        'english_proficiency': int(request.get('english_proficiency', '0').strip()),
        'native_lang': int(request.get('native_lang', '0').strip()),
        'address': int(request.get('address', '0').strip()),
        'other_address': request.get('other_address').strip(),
        'time_in_area': int(request.get('time_in_area', '0').strip()),
        'spoogler_relo': request.get('spoogler_relo').strip(),
        'transportation': int(request.get('transportation', '0').strip()),
        'side_driving': int(request.get('side_driving', '0').strip()),
        'events_size': [int(e) for e in request.get_all('events_size')],
        'event_types': [int(e) for e in request.get_all('event_types')],
        'event_types_other': request.get('event_types_other').strip(),
        'support_types': [int(s) for s in request.get_all('support_types')],
        'support_types_other': request.get('support_types_other').strip(),
        'support_others': [int(o) for o in request.get_all('support_others')],
        'support_others_other': request.get('support_others_other').strip(),
        'children_ages': [int(a) for a in request.get_all('children_ages')],
        'test': request.get('test', 'False').strip() == 'True',
        'user': user,
        'logout_url': logout_url,
        'not_on_google_group': int(request.get("not_on_google_group", '0')),
        'not_on_facebook': int(request.get("not_on_facebook", '0')),
        'not_on_fb_kidsZone': int(request.get("not_on_fb_kidsZone", '0')),
    })

