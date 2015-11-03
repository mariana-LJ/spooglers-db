from google.appengine.ext import ndb
from google.appengine.api import users

# List of ambassadors
ambassadors_list = [
    (0, "Spooglers Webmaster", "", "bayareaspooglers.webmaster@gmail.com"),
    (1, "Bay Area Spooglers", "", "bayareaspooglers@gmail.com"),
    (2, "Puja", "Sharma", "puja.sharma159@gmail.com"),
    (3, "Sarah", "Ison", "ison.sarahj@gmail.com")]

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
    support_others = ndb.IntegerProperty(repeated=True)  # See support_other_list
    support_others_other = ndb.StringProperty(repeated=False)  # Other type of support accessed by Spoogler
    kidszone_invite = ndb.BooleanProperty(default=True)  # Option to be invited to KidsZone Facebook group
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
        'support_others': [int(o) for o in request.get_all('support_others')],
        'support_others_other': request.get('support_others_other').strip(),
        'kidszone_invite': request.get('kidszone_invite', '0') == '1',
        'children_ages': [int(a) for a in request.get_all('children_ages')],
        'test': request.get('test', 'False').strip() == 'True',
        'user': user,
        'logout_url': logout_url,
        'not_on_google_group': int(request.get("not_on_google_group", '0')),
        'not_on_facebook': int(request.get("not_on_facebook", '0')),
        'not_on_fb_kidsZone': int(request.get("not_on_fb_kidsZone", '0')),
    })

