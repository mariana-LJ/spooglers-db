import webapp2
import os
import jinja2

import random

from models import Spoogler

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
  
  def _generate_token(self):
    return random.randint(11111, 99999)
  
app = webapp2.WSGIApplication([(r'/form', FormHandler)], debug = True)

