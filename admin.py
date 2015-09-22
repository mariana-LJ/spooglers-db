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
PAGE_SIZE = 5

class AdminHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""

    def get(self):
        """Displays the form for the Spoogler/Googler to fill out."""
        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.path)
        query = Spoogler.query()
        template_context = {'user': user,
                            'logout_url': logout_url,
                            'query': query
                            }

        # Initialize the template fields that contain multiple options in the form

        self.response.out.write(self._render_template('admin.html',
                                template_context))

    def post(self):
        logging.info(self.request.get("spoogler_email"))
        logging.info(self.request.get("action"))

    @classmethod
    def _render_template(cls, template_name, context=None):
        """It displays the form according to the template context given."""

        if context is None:
            context = {}

        template = JINJA_ENV.get_template(template_name)

        return template.render(context)

class FacebookHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""
    def post(self):
        logging.info(self.request.get("spoogler_email"))
        logging.info(self.request.get("action"))

#pylint: disable = C0103
app = webapp2.WSGIApplication([
    (r'/admin', AdminHandler),
    (r'/admin/facebook', FacebookHandler),],
    debug = True)

