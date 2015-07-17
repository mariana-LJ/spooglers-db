# Locally disabling the following messages in pylint: 
# E1101: Function %r has no %r member (This message may report object members 
# that are created dynamically, but exist at the time they are accessed.)
# F0401: Used when PyLint has been unable to import a module.
# E0602: Used when an undefined variable is accessed.
# C0103: Used when a name doesn't doesn't fit the naming convention associated 
# to its type (constant, variable, class…). Disabled for the "app" object 
# created at the end 
# Source: http://pylint-messages.wikidot.com/all-codes
#pylint: disable=E1101, F0401, E0602, C0103

"""This program contains the class that handles the logic to display and 
update the welcome membership form for the Spooglers group."""

import jinja2
import os
import webapp2

from google.appengine.api import mail
from google.appengine.ext import ndb
from models import Spoogler
from random import randint

JINJA_ENV = jinja2.Environment(loader = 
jinja2.FileSystemLoader(os.path.dirname(__file__)))


class FormHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""

    def get(self):
        """Displays the form for the Spoogler/Googler to fill out."""
        template_context = {'valid_form' : True}
        self.response.out.write(self._render_template('main.html', 
                                template_context))

    def post(self):
        """Validates the information placed on the form by the user. It also 
        calls the function to create an instance of a Spoogler in the Datastore 
        and displays messages according to what the user has written on the 
        fields of the form (success or failure)"""
        
        token_value = 0
        template_context = {
          'first_name': self.request.get('first_name').strip(), 
          'last_name': self.request.get('last_name').strip(), 
          'spoogler_email': self.request.get('spoogler_email').strip(), 
          'googler_email': self.request.get('googler_email').strip(),
        }
    
        if FormHandler._validate_form(template_context):
            template_context['valid_form'] = True
            token_value = FormHandler._generate_token()
            
            if self._create_spoogler(template_context, token_value):
                self._send_confirmation_email(template_context['googler_email'],
                                              token_value)
            template_context['first_name'] = ""
            template_context['last_name'] = ""
        else:
            template_context['valid_form'] = False
    
        self.response.out.write(FormHandler._render_template('main.html', 
                            template_context))

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
        if not template_context['first_name']:
            template_context['first_name_error'] = True
            result = False
        if not template_context['last_name']:
            template_context['last_name_error'] = True
            result = False
        if not template_context['spoogler_email']:
            template_context['spoogler_email_error'] = True
            result = False
        if not template_context['googler_email']:
            template_context['googler_email_error'] = True
            result = False
        return result
    
    @classmethod
    def _generate_token(cls):
        """Generates a token for the customized confirmation link."""
        
        return randint(111111, 999999)
        
    def _send_confirmation_email(self, googler_email, token_value):
        """After the form was filled out successfully, a confirmation email 
        is sent to the Googler's email (@google.com) that contains a customized 
        confirmation url. When the Googler clicks on this url, the Spoogler is 
        verified and marked as 'Active'/'Verified' in the database"""
        
        sender_address = "Spooglers Webmaster \
                         <bayareaspooglers.webmaster@gmail.com>"
        subject = "Test"
        body = "Test spoogler_email "
        body += "<a href=https://'" + self.request.host + "/confirm.html?g=" + \
                googler_email + "&t=" + str(token_value) + \
                "'>click to confirm</a>"
        mail.send_mail(sender_address, googler_email, subject, body)
        
    @ndb.transactional
    def _create_spoogler(self, template_context, token_value):
        """Creates an instance of a Spoogler in the Datastore."""
        
        write_success = False
        #instantiation of the Spoogler class:
        spoogler = Spoogler(first_name = template_context['first_name'], 
                   last_name = template_context['last_name'], 
                   spoogler_email = template_context['spoogler_email'], 
                   googler_email = template_context['googler_email'],
                   status = 'inactive', 
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
    """An experimental class to start building a confirmation for the Googler's 
    email."""
    
    def get(self):
        """This function takes two parameters from the given URL: the googler's 
        email and a pseudo-randomly generated token and displays a confirmation 
        message of the activation of the new Spoogler."""
    
        template_context = {'googler': self.request.get('g'),
                            'token': self.request.get('t')}
        self.response.out.write(self._render_template('confirmation.html', 
                            template_context))

    def post(self):
        """A dummy method to avoid formatting errors when using pylint."""
        pass
    
    @classmethod
    def _render_template(cls, template_name, context=None):
        """It displays the webpage according to the information inside the 
        dictionary or context."""
    
        if context is None:
            context = {}
    
        template = JINJA_ENV.get_template(template_name)
    
        return template.render(context)

    def __init__(self):
        pass


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


app = webapp2.WSGIApplication([(r'/welcome_form\.html', FormHandler),
                               (r'/confirm\.html', ConfirmHandler),
                               (r'/thankyou\.html', EmailHandler), 
                              ], debug = True)

