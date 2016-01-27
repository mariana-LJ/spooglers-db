# coding=utf-8
import logging
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

# Spoogler countries
countries_list = [
    (0, "Please select"),
    (1, "United States of America"),
    (2, "Afghanistan"),
    (3, "Albania"),
    (4, "Algeria"),
    (5, "American Samoa"),
    (6, "Andorra"),
    (7, "Angola"),
    (8, "Anguilla"),
    (9, "Antigua and Barbuda"),
    (10, "Argentina"),
    (11, "Armenia"),
    (12, "Aruba"),
    (13, "Australia"),
    (14, "Austria"),
    (15, "Azerbaijan"),
    (16, "Bahamas"),
    (17, "Bahrain"),
    (18, "Bangladesh"),
    (19, "Barbados"),
    (20, "Belarus"),
    (21, "Belgium"),
    (22, "Belize"),
    (23, "Benin"),
    (24, "Bermuda"),
    (25, "Bhutan"),
    (26, "Bolivia"),
    (27, "Bosnia and Herzegovina"),
    (28, "Botswana"),
    (29, "Brazil"),
    (30, "British Virgin Islands"),
    (31, "Brunei"),
    (32, "Bulgaria"),
    (33, "Burkina Faso"),
    (34, "Burma"),
    (35, "Burundi"),
    (36, "Cambodia"),
    (37, "Cameroon"),
    (38, "Canada"),
    (39, "Cape Verde"),
    (40, "Cayman Islands"),
    (41, "Central African Republic"),
    (42, "Chad"),
    (43, "Chile"),
    (44, "China"),
    (45, "Christmas Island"),
    (46, "Cocos Islands"),
    (47, "Colombia"),
    (48, "Comoros"),
    (49, "Cook Islands"),
    (50, "Costa Rica"),
    (51, u"Côte d'Ivoire"),
    (52, "Croatia"),
    (53, "Cuba"),
    (54, u"Curaçao"),
    (55, "Cyprus"),
    (56, "Czech Republic"),
    (57, "Democratic Republic of the Congo"),
    (58, "Denmark"),
    (59, "Djibouti"),
    (60, "Dominica"),
    (61, "Dominican Republic"),
    (62, "East Timor"),
    (63, "Ecuador"),
    (64, "Egypt"),
    (65, "El Salvador"),
    (66, "Equatorial Guinea"),
    (67, "Eritrea"),
    (68, "Estonia"),
    (69, "Ethiopia"),
    (70, "Falkland Islands"),
    (71, "Faroe Islands"),
    (72, "Fiji"),
    (73, "Finland"),
    (74, "France"),
    (75, "French Guiana"),
    (76, "French Polynesia"),
    (77, "Gabon"),
    (78, "The Gambia"),
    (79, "Georgia"),
    (80, "Germany"),
    (81, "Ghana"),
    (82, "Gibraltar"),
    (83, "Greece"),
    (84, "Greenland"),
    (85, "Grenada"),
    (86, "Guadeloupe"),
    (87, "Guam"),
    (88, "Guatemala"),
    (89, "Guernsey"),
    (90, "Guinea"),
    (91, "Guinea-Bissau"),
    (92, "Guyana"),
    (93, "Haiti"),
    (94, "Honduras"),
    (95, "Hong Kong"),
    (96, "Hungary"),
    (97, "Iceland"),
    (98, "India"),
    (99, "Indonesia"),
    (100, "Iran"),
    (101, "Iraq"),
    (102, "Ireland"),
    (103, "Isle of Man"),
    (104, "Israel"),
    (105, "Italy"),
    (106, "Jamaica"),
    (107, "Japan"),
    (108, "Jersey"),
    (109, "Jordan"),
    (110, "Kazakhstan"),
    (111, "Kenya"),
    (112, "Kiribati"),
    (113, "Kosovo"),
    (114, "Kuwait"),
    (115, "Kyrgyzstan"),
    (116, "Laos"),
    (117, "Latvia"),
    (118, "Lebanon"),
    (119, "Lesotho"),
    (120, "Liberia"),
    (121, "Libya"),
    (122, "Liechtenstein"),
    (123, "Lithuania"),
    (124, "Luxembourg"),
    (125, "Macedonia"),
    (126, "Madagascar"),
    (127, "Malawi"),
    (128, "Malaysia"),
    (129, "Maldives"),
    (130, "Mali"),
    (131, "Malta"),
    (132, "Marshall Islands"),
    (133, "Martinique"),
    (134, "Mauritania"),
    (135, "Mauritius"),
    (136, "Mayotte"),
    (137, "Mexico"),
    (138, "Federated States of Micronesia"),
    (139, "Moldova"),
    (140, "Monaco"),
    (141, "Mongolia"),
    (142, "Montenegro"),
    (143, "Montserrat"),
    (144, "Morocco"),
    (145, "Mozambique"),
    (146, "Nagorno-Karabakh"),
    (147, "Namibia"),
    (148, "Nauru"),
    (149, "Nepal"),
    (150, "Netherlands"),
    (151, "New Caledonia"),
    (152, "New Zealand"),
    (153, "Nicaragua"),
    (154, "Niger"),
    (155, "Nigeria"),
    (156, "Niue"),
    (157, "Norfolk Island"),
    (158, "North Korea"),
    (159, "Northern Cyprus"),
    (160, "Northern Mariana Islands"),
    (161, "Norway"),
    (162, "Oman"),
    (163, "Pakistan"),
    (164, "Palau"),
    (165, "Palestine"),
    (166, "Panama"),
    (167, "Papua New Guinea"),
    (168, "Paraguay"),
    (169, "Peru"),
    (170, "Philippines"),
    (171, "Pitcairn Islands"),
    (172, "Poland"),
    (173, "Portugal"),
    (174, "Puerto Rico"),
    (175, "Qatar"),
    (176, "Republic of the Congo"),
    (177, u"Réunion"),
    (178, "Romania"),
    (179, "Russia"),
    (180, "Rwanda"),
    (181, "Sahrawi Arab Democratic Republic"),
    (182, u"Saint Barthélemy"),
    (183, "Saint Helena, Ascension and Tristan da Cunha"),
    (184, "Saint Kitts and Nevis"),
    (185, "Saint Martin"),
    (186, "Saint Lucia"),
    (187, "Saint Pierre and Miquelon"),
    (188, "Saint Vincent and the Grenadines"),
    (189, "Samoa"),
    (190, "San Marino"),
    (191, u"São Tomé and Príncipe"),
    (192, "Saudi Arabia"),
    (193, "Senegal"),
    (194, "Serbia"),
    (195, "Seychelles"),
    (196, "Sierra Leone"),
    (197, "Singapore"),
    (198, "Sint Maarten"),
    (199, "Slovakia"),
    (200, "Slovenia"),
    (201, "Solomon Islands"),
    (202, "Somalia"),
    (203, "Somaliland"),
    (204, "South Africa"),
    (205, "South Korea"),
    (206, "South Sudan"),
    (207, "Spain"),
    (208, "Sri Lanka"),
    (209, "Sudan"),
    (210, "Suriname"),
    (211, "Svalbard"),
    (212, "Swaziland"),
    (213, "Sweden"),
    (214, "Switzerland"),
    (215, "Syria"),
    (216, "Taiwan"),
    (217, "Tajikistan"),
    (218, "Tanzania"),
    (219, "Thailand"),
    (220, "Togo"),
    (221, "Tokelau"),
    (222, "Tonga"),
    (223, "Transnistria"),
    (224, "Trinidad and Tobago"),
    (225, "Tunisia"),
    (226, "Turkey"),
    (227, "Turkmenistan"),
    (228, "Turks and Caicos Islands"),
    (229, "Tuvalu"),
    (230, "Uganda"),
    (231, "Ukraine"),
    (232, "United Arab Emirates"),
    (233, "United Kingdom"),
    (234, "United States Virgin Islands"),
    (235, "Uruguay"),
    (236, "Uzbekistan"),
    (237, "Vanuatu"),
    (238, "Vatican City"),
    (239, "Venezuela"),
    (240, "Vietnam"),
    (241, "Wallis and Futuna"),
    (242, "Yemen"),
    (243, "Zambia"),
    (244, "Zimbabwe"),
]

# States for US Spooglers
us_states_list = [
    (0, "Please select", "select"),
    (1, "Alabama", "AL"),
    (2, "Alaska", "AK"),
    (3, "Arizona", "AZ"),
    (4, "Arkansas", "AR"),
    (5, "California", "CA"),
    (6, "Colorado", "CO"),
    (7, "Connecticut", "CT"),
    (8, "Delaware", "DE"),
    (9, "Florida", "FL"),
    (10, "Georgia", "GA"),
    (11, "Hawaii", "HI"),
    (12, "Idaho", "ID"),
    (13, "Illinois", "IL"),
    (14, "Indiana", "IN"),
    (15, "Iowa", "IA"),
    (16, "Kansas", "KS"),
    (17, "Kentucky", "KY"),
    (18, "Louisiana", "LA"),
    (19, "Maine", "ME"),
    (20, "Maryland", "MD"),
    (21, "Massachusetts", "MA"),
    (22, "Michigan", "MI"),
    (23, "Minnesota", "MN"),
    (24, "Mississippi", "MS"),
    (25, "Missouri", "MO"),
    (26, "Montana", "MT"),
    (27, "Nebraska", "NE"),
    (28, "Nevada", "NV"),
    (29, "New Hampshire", "NH"),
    (30, "New Jersey", "NJ"),
    (31, "New Mexico", "NM"),
    (32, "New York", "NY"),
    (33, "North Carolina", "NC"),
    (34, "North Dakota", "ND"),
    (35, "Ohio", "OH"),
    (36, "Oklahoma", "OK"),
    (37, "Oregon", "OR"),
    (38, "Pennsylvania", "PA"),
    (39, "Rhode Island", "RI"),
    (40, "South Carolina", "SC"),
    (41, "South Dakota", "SD"),
    (42, "Tennessee", "TN"),
    (43, "Texas", "TX"),
    (44, "Utah", "UT"),
    (45, "Vermont", "VT"),
    (46, "Virginia", "VA"),
    (47, "Washington", "WA"),
    (48, "West Virginia", "WV"),
    (49, "Wisconsin", "WI"),
    (50, "Wyoming", "WY"),
]

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

# Invitation to the Facebook KidsZone group
kidszone_options_list = [
    (0, "Please select"),
    (1, "Yes"),
    (2, "No")]

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
    same_as_spoogler_email = ndb.IntegerProperty(repeated=False)
    googler_full_name = ndb.StringProperty(repeated=False)
    googler_ldap = ndb.StringProperty()
    spoogler_country = ndb.IntegerProperty(repeated=False)
    spoogler_us_state = ndb.IntegerProperty(repeated=False)  # See us_states_list
    work_status = ndb.IntegerProperty(repeated=False)  # See work_status_list
    english_proficiency = ndb.IntegerProperty(repeated=False)  # See proficiency_list
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
    template_context['countries_list'] = countries_list
    template_context['work_status_list'] = work_status_list
    template_context['languages_list'] = languages_list
    template_context['us_states_list'] = us_states_list
    template_context['proficiency_list'] = proficiency_list
    template_context['address_list'] = address_options_list
    template_context['times_list'] = times_list
    template_context['support_other_list'] = support_other_list
    template_context['kidszone_options_list'] = kidszone_options_list
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
        'same_as_spoogler_email': int(request.get('same_as_spoogler_email', '0').strip()),
        #'spoogler_fb_email': request.get('spoogler_fb_email').strip(),
        'googler_full_name': request.get('googler_full_name').strip(),
        'googler_ldap': request.get('googler_ldap').strip(),
        'spoogler_country': int(request.get('spoogler_country', '0').strip()),
        'spoogler_us_state': int(request.get('spoogler_us_state', '0').strip()),
        'work_status': int(request.get('work_status', '0').strip()),
        'english_proficiency': int(request.get('english_proficiency', '0').strip()),
        'native_lang': int(request.get('native_lang', '0').strip()),
        'address': int(request.get('address', '0').strip()),
        'other_address': request.get('other_address').strip(),
        'time_in_area': int(request.get('time_in_area', '0').strip()),
        'spoogler_relo': request.get('spoogler_relo').strip(),
        'support_others': [int(o) for o in request.get_all('support_others')],
        'support_others_other': request.get('support_others_other').strip(),
        'kidszone_invite': int(request.get('kidszone_invite', '0').strip()),
        'children_ages': [int(a) for a in request.get_all('children_ages')],
        'test': request.get('test', 'False').strip() == 'True',  # to set test flag, append ?test=True to the URL
        'user': user,
        'logout_url': logout_url,
        'not_on_groups': int(request.get("not_on_groups", '0')),
        'email_lists': int(request.get("email_lists", '0')),
        'show_only_active': int(request.get("show_only_active", '0')),
        'show_all_cols': int(request.get("show_all_cols", '0')),
    })

    if template_context['same_as_spoogler_email']:
        template_context['spoogler_fb_email'] = template_context['spoogler_email']
    else:
        template_context['spoogler_fb_email'] = request.get('spoogler_fb_email').strip()
