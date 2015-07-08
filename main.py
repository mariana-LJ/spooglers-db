import webapp2
import os
import jinja2

import random

from models import Spoogler
from google.appengine.api import mail

jinja_env = jinja2.Environment(loader = 
jinja2.FileSystemLoader(os.path.dirname(__file__)))

class FormHandler(webapp2.RequestHandler):
  def get(self):
    template_context = {}
    self.response.out.write(self._render_template('main.html', 
                            template_context))

  def post(self):
    template_context = {'firstname': self.request.get('firstn'), 
    'lastname': self.request.get('lastn'), 
    'email': self.request.get('email'), 
    'googlremail': self.request.get('googlr'),
    'greeting' : 'Hello',
    }
    
    #instantiation of the Spoogler class:
    spoogler = Spoogler(firstName = self.request.get('firstn'), 
                        lastName = self.request.get('lastn'), 
                        email = self.request.get('email'), 
                        googlerEmail = self.request.get('googlr'),
                        status = 'inactive', 
                        token = self._generate_token())
                        
    # An entity is persisted in the Datastore:
    spoogler.put()
        
    self.response.out.write(self._render_template('main.html', 
                            template_context))
  
  def _render_template(self, template_name, context=None):
    if context is None:
      context = {}
    
    template = jinja_env.get_template(template_name)
    
    return template.render(context)
  
class ConfirmHandler(webapp2.RequestHandler):
  def get(self):
    template_context = {'user': self.request.get('u'),
                        'token': self.request.get('t')}
    self.response.out.write(self._render_template('confirmation.html', 
                            template_context))
                            
  def _render_template(self, template_name, context=None):
    if context is None:
      context = {}
    
    template = jinja_env.get_template(template_name)
    
    return template.render(context)

class EmailHandler(webapp2.RequestHandler):
  def post(self):
    email = "mlopezj14@gmail.com"
    
    sender_address = "Spooglers Webmaster <bayareaspooglers.webmaster@gmail.com>"
    subject = "Test"
    body = "Test email"
    mail.send_mail(sender_address, email, subject, body)
    
app = webapp2.WSGIApplication([(r'/welcome_form\.html', FormHandler),
                               (r'/confirm\.html', ConfirmHandler),
                              ], debug = True)

