"""This program contains the class that handles the logic to display and 
update the welcome membership form for the Spooglers group.

To avoid pylint errors, the following messages in pylint were disabled: 
E1101: Function %r has no %r member (This message may report object members 
that are created dynamically, but exist at the time they are accessed.)
F0401: Used when PyLint has been unable to import a module.
E0602: Used when an undefined variable is accessed.
C0103: Used when a name doesn't doesn't fit the naming convention associated 
to its type (constant, variable, class). Disabled for the "app" object 
created at the end """

__author__ = 'bayareaspooglers.webmaster@gmail.com'

#pylint: disable=E1101, F0401, E0602
#Source: http://pylint-messages.wikidot.com/all-codes

import jinja2
import os
import webapp2
import re
import logging

from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import users

from models import Spoogler
from models import work_status_list
from models import languages_list
from models import proficiency_list
from models import address_options_list
from models import times_list
from models import transportation_list
from models import side_driving_list
from models import event_size_list
from models import event_type_list
from models import support_type_list
from models import support_other_list
from models import children_ages_list
from random import randint

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class FormHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""

    def get(self):
        """Displays the form for the Spoogler/Googler to fill out."""
        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.path)
        template_context = {'valid_form': True,
                            'successful_submission': False,
                            'user': user,
                            'logout_url': logout_url,
                            }

        # Initialize the template fields that contain multiple options in the form
        self._init_multiple_options(template_context)
        self.response.out.write(self._render_template('main.html', 
                                template_context))

    def post(self):
        """Validates the information placed on the form by the user. It also 
        calls the function to create an instance of a Spoogler in the Datastore 
        and displays messages according to what the user has written on the 
        fields of the form (success or failure)"""
        
        token_value = 0
        template_context = self._get_context()

        # Initialize the template fields that contain multiple options in the form
        self._init_multiple_options(template_context)

        if FormHandler._validate_form(template_context):
            template_context['valid_form'] = True
            token_value = FormHandler._generate_token()
            
            if self._create_spoogler(template_context, token_value):
                self._send_confirmation_email(template_context['googler_ldap'],
                                              token_value)

            FormHandler._clean_context(template_context)

        else:
            template_context['valid_form'] = False
    
        self.response.out.write(FormHandler._render_template('main.html', 
                            template_context))

    def _get_context(self):
        """ Read the information from the form to build the context.
        :param template_context
        :return:
        """
        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.path)
        template_context = {
            # Basic information
            'full_name': self.request.get('full_name').strip(),
            'spoogler_email': self.request.get('spoogler_email').strip(),
            'spoogler_fb_email': self.request.get('spoogler_fb_email').strip(),
            'googler_ldap': self.request.get('googler_ldap').strip(),
            'spoogler_country': self.request.get('spoogler_country').strip(),
            'work_status': int(self.request.get('work_status').strip()),
            'languages': [self.request.get('spoogler_lang'+str(i)) for i in range(0, 5)],
            'lang_proficiencies': [int(self.request.get('spoogler_lang_prof'+str(i))) for i in range(0, 5)],
            'address': int(self.request.get('address').strip()),
            'other_address': self.request.get('other_address').strip(),
            'time_in_area': int(self.request.get('time_in_area').strip()),
            'spoogler_relo': self.request.get('spoogler_relo').strip(),
            'transportation': int(self.request.get('transportation').strip()),
            'side_driving': int(self.request.get('side_driving').strip()),
            'events_size': [int(e) for e in self.request.get_all('events_size')],
            'event_types': [int(e) for e in self.request.get_all('event_types')],
            'event_types_other': self.request.get('event_types_other').strip(),
            'support_types': [int(s) for s in self.request.get_all('support_types')],
            'support_types_other': self.request.get('support_types_other').strip(),
            'support_others': [int(o) for o in self.request.get_all('support_others')],
            'support_others_other': self.request.get('support_others_other').strip(),
            'children_ages': [int(a) for a in self.request.get_all('children_ages')],
            'user': user,
            'logout_url': logout_url,
        }

        # Forcing the first language to be English (since the "disabled" property does not allow to get the
        # value of the spoogler_lang0 field from the html form)
        template_context['languages'][0] = 'English'

        return template_context

    @classmethod
    def _render_template(cls, template_name, context=None):
        """It displays the form according to the template context given."""
        
        if context is None:
            context = {}
    
        template = JINJA_ENV.get_template(template_name)
    
        return template.render(context)
  
    @classmethod
    def _validate_form(cls, template_context):
        """Verifies that the information entered in the form is complete and 
        correct according to the instructions."""
        result = True
        mail_re = re.compile(r'^.+@.+$')
        at_sign_re = re.compile(r'@')
        # Verify that the user entered information in the fields:
        if not template_context['full_name']:
            template_context['full_name_error'] = True
            result = False
        if not template_context['spoogler_email'] or \
           not mail_re.search(template_context['spoogler_email']):
            template_context['spoogler_email_error'] = True
            result = False
        # Check uniqueness of spoogler_email
        if template_context['spoogler_email']:
            spoogler_email_qry = Spoogler.query(Spoogler.spoogler_email == \
                                 template_context['spoogler_email']).fetch()
            if spoogler_email_qry:
                template_context['spoogler_email_error'] = True
                template_context['spoogler_email_duplicate'] = True
                result = False
        if not template_context['googler_ldap'] or \
           at_sign_re.search(template_context['googler_ldap']):
            template_context['googler_ldap_error'] = True
            result = False
        # Check uniqueness of googler_ldap
        if template_context['googler_ldap']:
            googler_ldap_qry = Spoogler.query(Spoogler.googler_ldap == \
                               template_context['googler_ldap']).fetch()
            if googler_ldap_qry:
                template_context['googler_ldap_error'] = True
                template_context['googler_ldap_duplicate'] = True
                result = False
        
        return result
    
    @classmethod
    def _generate_token(cls):
        """Generates a token for the customized confirmation link."""
        
        return randint(111111, 999999)
        
    def _send_confirmation_email(self, googler_ldap, token_value):
        """After the form was filled out successfully, a confirmation email 
        is sent to the Googler's email (@google.com) that contains a customized 
        confirmation url. When the Googler clicks on this url, the Spoogler is 
        verified and marked as 'Active'/'Verified' in the database"""
        
        sender_address = "Spooglers Webmaster \
                         <bayareaspooglers.webmaster@gmail.com>"
        email_domain_name = "@gmail.com"
        googler_email = "mlopezj14@gmail.com"  # googler_ldap + email_domain_name
        subject = "Spooglers Welcome form test"
        body = "Test with googler email."
        body += "<a href=\"https://" + self.request.host + \
                "/confirm?g=" + \
                googler_ldap + "&t=" + str(token_value) + \
                "\">click to confirm</a>"
        mail.send_mail(sender_address, googler_email, subject, body)
        
    @ndb.transactional
    def _create_spoogler(self, template_context, token_value):
        """Creates an instance of a Spoogler in the Datastore."""
        
        write_success = False
        # Instantiation of the Spoogler class:
        spoogler = Spoogler(
                    full_name = template_context['full_name'],
                    spoogler_email = template_context['spoogler_email'],
                    spoogler_fb_email = template_context['spoogler_fb_email'],
                    googler_ldap = template_context['googler_ldap'],
                    spoogler_country = template_context['spoogler_country'],
                    work_status = template_context['work_status'],
                    languages = template_context['languages'],
                    lang_proficiencies = template_context['lang_proficiencies'],
                    address = template_context['address'],
                    other_address = template_context['other_address'],
                    time_in_area = template_context['time_in_area'],
                    spoogler_relo = template_context['spoogler_relo'],
                    transportation = template_context['transportation'],
                    side_driving = template_context['side_driving'],
                    events_size = template_context['events_size'],
                    event_types = template_context['event_types'],
                    event_types_other = template_context['event_types_other'],
                    support_types = template_context['support_types'],
                    support_types_other = template_context['support_types_other'],
                    support_others = template_context['support_others'],
                    support_others_other = template_context['support_others_other'],
                    children_ages = template_context['children_ages'],
                    status = 'inactive',
                    token = token_value)
                        
        # An entity is persisted in the Datastore:
        try:
            spoogler.put()
            write_success = True
        except datastore_errors.TransactionFailedError:
            self.response.out.write('Something went wrong, please try again')
        return write_success

    def _init_multiple_options(self, template_context):
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

    @classmethod
    def _clean_context(cls, template_context):
        """ Resets the fields of the template context after successful
        submission."""
        template_context['full_name'] = ""
        template_context['spoogler_email'] = ""
        template_context['spoogler_fb_email'] = ""
        template_context['googler_ldap'] = ""
        template_context['spoogler_country'] = ""
        template_context['work_status'] = 0
        template_context['languages'] = []
        template_context['lang_proficiencies'] = []
        template_context['address'] = 0
        template_context['other_address'] = ""
        template_context['time_in_area'] = 0
        template_context['spoogler_relo'] = ""
        template_context['transportation'] = 0
        template_context['side_driving'] = 0
        template_context['events_size'] = []
        template_context['event_types'] = []
        template_context['event_types_other'] = ""
        template_context['support_types'] = []
        template_context['support_types_other'] = ""
        template_context['support_others'] = []
        template_context['support_others_other'] = ""
        template_context['children_ages'] = []
        template_context['successful_submission'] = True

        # Clean error flags
        template_context['full_name_error'] = False
        template_context['spoogler_email_error'] = False
        template_context['spoogler_email_duplicate'] = False
        template_context['googler_ldap_error'] = False

    def __init__(self, request, response):
        self.initialize(request, response)

class ConfirmHandler(webapp2.RequestHandler):
    """A class to start building a confirmation for the Googler's ldap."""
    
    def get(self):
        """This function takes two parameters from the given URL: the googler's 
        email and a pseudo-randomly generated token and displays a confirmation 
        message of the activation of the new Spoogler."""
        
        template_context = {'googler': self.request.get('g').strip(),
                            'token': int(self.request.get('t').strip())}
         
        # The status of the Spoogler changes from inactive to active
        spoogler = Spoogler.query(Spoogler.googler_ldap == \
                   template_context['googler']).fetch()
        if spoogler:
            if template_context['token'] == spoogler[0].token:
                if spoogler[0].status != 'inactive':
                    template_context['confirmation_message'] = 'The Spoogler ' \
                    'is already an active member on this group.'
                else:
                    if self._activate_spoogler(spoogler[0]):
                        template_context['confirmation_message'] = \
                        'Congratulations! The Spoogler is now an active ' \
                        'member of this group and has received a Welcome email.'
                        self._send_welcome_email(template_context)
            else:
                template_context['confirmation_message'] = 'Wrong information.'\
                ' Please contact us: bayareaspooglers.webmaster@gmail.com'
        else:
            template_context['confirmation_message'] = 'Wrong information.'\
                ' Please contact us: bayareaspooglers.webmaster@gmail.com'
        
        self.response.out.write(self._render_template('confirmation.html', 
                            template_context))        

    def post(self):
        """A dummy method to avoid formatting errors when using pylint."""
        pass
    
    @ndb.transactional
    def _activate_spoogler(self, spoogler):
        """It changes the status of the Spoogler from 'inactive' to 'active' 
        using a query."""
        spoogler.status = 'active'
        activation_success = False
        try:
            spoogler.put()
            activation_success = True
        except datastore_errors.TransactionFailedError:
            self.response.out.write('Something went wrong, please try again')
        
        return activation_success
        
    def _send_welcome_email(self, template_context):
        """It sends a Welcome email once the new spoogler has been successfully
        activated by the Googler."""
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap == \
                       template_context['googler']).fetch()
        sender_email = "Spooglers Webmaster \
                       <bayareaspooglers.webmaster@gmail.com>"
        recipient_email = spoogler_qry[0].spoogler_email
        subject = "Welcome to the Bay Area Spooglers group"
        body = "Welcome to the Bay Area Spooglers group."
        mail.send_mail(sender_email, recipient_email, subject, body)
    
    @classmethod
    def _render_template(cls, template_name, context=None):
        """It displays the webpage according to the information inside the 
        dictionary or context."""
    
        if context is None:
            context = {}
    
        template = JINJA_ENV.get_template(template_name)
    
        return template.render(context)

    def __init__(self, request, response):
        self.initialize(request, response)


class EmailHandler(webapp2.RequestHandler):
    """An experimental class to verify the process of sending email."""
    
    def get(self):
        """This function builds the elements necessary to send an email using 
        the email api in App Engine."""
    
        email = "mlopezj14@gmail.com"
    
        sender_address = "Spooglers Webmaster \
                         <bayareaspooglers.webmaster@gmail.com>"
        subject = "Test"
        body = "Test email"
        mail.send_mail(sender_address, email, subject, body)
        template_context = {}
        self.response.out.write(self._render_template('thankyou.html', 
                            template_context))
    
    def post(self):
        """A dummy method to avoid formatting errors when using pylint."""
        pass
    
    @classmethod                            
    def _render_template(cls, template_name, context=None):
        """Displays a webpage according to the information contained in the 
        dictionary or context."""
    
        if context is None:
            context = {}
    
        template = JINJA_ENV.get_template(template_name)
    
        return template.render(context)

    def __init__(self):
        pass

#pylint: disable = C0103
app = webapp2.WSGIApplication([
    (r'/', FormHandler),
    (r'/signup', FormHandler),
    (r'/confirm', ConfirmHandler),],
    debug=True)

