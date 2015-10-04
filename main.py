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
from google.appengine.api import datastore_errors

from models import Spoogler
from models import init_multiple_options
from models import get_spoogler_context
from random import randint

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class FormHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""

    def get(self):
        """Displays the form for the Spoogler/Googler to fill out."""
        # Initialize default options
        template_context = {}
        get_spoogler_context(self.request, template_context)
        template_context['valid_form'] = True
        template_context['successful_submission'] = False
        template_context['confirmation_ldap'] = ""

        # Initialize the template fields that contain multiple options in the form
        init_multiple_options(template_context)
        self.response.out.write(self._render_template('main.html', 
                                template_context))

    def post(self):
        """Validates the information placed on the form by the user. It also 
        calls the function to create an instance of a Spoogler in the Datastore 
        and displays messages according to what the user has written on the 
        fields of the form (success or failure)"""
        
        token_value = 0
        template_context = {}
        get_spoogler_context(self.request, template_context)
        template_context['confirmation_ldap'] = template_context['googler_ldap']

        # Initialize the template fields that contain multiple options in the form
        init_multiple_options(template_context)

        if FormHandler._validate_form(template_context):
            template_context['valid_form'] = True
            token_value = FormHandler._generate_token()
            
            if self._create_spoogler(template_context, token_value):
                self._send_confirmation_email(template_context['googler_ldap'],
                                              template_context['test'],
                                              token_value)

            FormHandler._clean_context(template_context)

        else:
            template_context['valid_form'] = False
    
        self.response.out.write(FormHandler._render_template('main.html', 
                            template_context))

    @classmethod
    def _clean_context(cls, template_context):
        """ Resets the fields of the template context after successful
        submission."""
        template_context['full_name'] = ""
        template_context['spoogler_email'] = ""
        template_context['spoogler_fb_email'] = ""
        template_context['googler_ldap'] = ""
        template_context['googler_full_name'] = ""
        template_context['spoogler_country'] = ""
        template_context['work_status'] = 0
        template_context['english_proficiency'] = 0
        template_context['native_lang'] = 0
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
        template_context['fb_email_error'] = False
        template_context['fb_email_duplicate'] = False
        template_context['googler_ldap_error'] = False

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
            spoogler_email_qry = Spoogler.query(Spoogler.spoogler_email ==
                                 template_context['spoogler_email']).fetch()
            if spoogler_email_qry:
                template_context['spoogler_email_error'] = True
                template_context['spoogler_email_duplicate'] = True
                result = False
        # Check uniqueness of spoogler_fb_email
        if template_context['spoogler_fb_email']:
            if not mail_re.search(template_context['spoogler_fb_email']):
                template_context['fb_email_error'] = True
                result = False
            fb_email_qry = Spoogler.query(Spoogler.spoogler_fb_email ==
                           template_context['spoogler_fb_email']).fetch()
            if fb_email_qry:
                template_context['fb_email_error'] = True
                template_context['fb_email_duplicate'] = True
                result = False
        if not template_context['googler_ldap']:
            template_context['googler_ldap_error'] = True
            result = False
        # Check that the user entered just the ldap (without the @google.com)
        if at_sign_re.search(template_context['googler_ldap']):
            template_context['ldap_at_sign_error'] = True
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
        
    def _send_confirmation_email(self, googler_ldap, test, token_value):
        """After the form was filled out successfully, a confirmation email 
        is sent to the Googler's email (@google.com) that contains a customized 
        confirmation url. When the Googler clicks on this url, the Spoogler is 
        verified and marked as 'Active'/'Verified' in the database"""
        
        sender_address = "Spooglers Webmaster \
                         <bayareaspooglers.webmaster@gmail.com>"
        email_domain_name = "@google.com"
        googler_email = googler_ldap + email_domain_name
        if test:
            googler_email = "mlopezj14@gmail.com"
        confirmation_url = "https://" + self.request.host + "/confirm?g=" + \
            googler_ldap + "&t=" + str(token_value)
        subject = "Spooglers Welcome form test"
        body = """
        Your spouse/partner has requested to join the Bay Area Spooglers
        (spouses of Googlers) Group. Please confirm your spouse/partner's
        subscription by clicking on the link below:

        %s
        """ % confirmation_url

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
                    googler_full_name = template_context['googler_full_name'],
                    googler_ldap = template_context['googler_ldap'],
                    spoogler_country = template_context['spoogler_country'],
                    work_status = template_context['work_status'],
                    english_proficiency = template_context['english_proficiency'],
                    native_lang = template_context['native_lang'],
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
                    test = template_context['test'],
                    status = 0,
                    token = token_value)
                        
        # An entity is persisted in the Datastore:
        try:
            spoogler.put()
            write_success = True
        except datastore_errors.TransactionFailedError:
            self.response.out.write('Something went wrong, please try again')
        return write_success

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
                if spoogler[0].status != 0:
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
        spoogler.status = 1
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
        if spoogler_qry[0].test:
            recipient_email = "mlopezj14@gmail.com"
        subject = "Welcome to the Bay Area Spooglers group"
        body = "Welcome to the Bay Area Spooglers group: " + spoogler_qry[0].full_name
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

#pylint: disable = C0103
app = webapp2.WSGIApplication([
    (r'/', FormHandler),
    (r'/signup', FormHandler),
    (r'/confirm', ConfirmHandler),],
    debug=True)

