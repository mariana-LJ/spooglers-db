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
from models import init_multiple_options
from models import get_spoogler_context

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
PAGE_SIZE = 5


class AdminHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""

    def get(self):
        """Displays the form for the Spoogler/Googler to fill out."""
        template_context = {}
        get_spoogler_context(self.request, template_context)
        query = Spoogler.query()
        query = query.order(-Spoogler.date_created).order(Spoogler.full_name)
        template_context['query'] = query
        self.update(template_context)

    def post(self):
        # get context
        template_context = {}
        get_spoogler_context(self.request, template_context)
        not_added_website = self.request.get("not_added_website")

        # build query
        query = Spoogler.query()
        if not_added_website:
            query = query.filter(Spoogler.website_status == False)
        if template_context['native_lang'] != 0:
            query = query.filter(Spoogler.native_lang == template_context['native_lang'])
        query = query.order(-Spoogler.date_created).order(Spoogler.full_name)
        template_context['query'] = query

        self.update(template_context)

    def update(self, template_context):
        init_multiple_options(template_context)

        self.response.out.write(self._render_template('admin.html',
                                template_context))

    @classmethod
    def _render_template(cls, template_name, context=None):
        """It displays the form according to the template context given."""

        if context is None:
            context = {}

        template = JINJA_ENV.get_template(template_name)

        return template.render(context)

# Handler for AJAX requests
class FacebookHandler(webapp2.RequestHandler):
    """This is the handler to display the Spooglers membership form."""
    def post(self):
        logging.info(self.request.get("spoogler_email"))
        logging.info(self.request.get("action"))


class FacebookKidsHandler(webapp2.RequestHandler):
    """ Handles the event where the administrator selects a checkbox
        when the Spoogler has been invited to the Facebook KidsZone group."""
    def post(self):
        logging.info(self.request.get("spoogler_email"))
        logging.info(self.request.get("action"))


class WebsiteGroupHandler(webapp2.RequestHandler):
    """ Handles the event where the administrator selects a checkbox
        when the Spoogler has been invited to the Google group to see
        the Spooglers official website."""
    def post(self):
        logging.info(self.request.get("spoogler_email"))
        logging.info(self.request.get("action"))


# pylint: disable = C0103

app = webapp2.WSGIApplication([
    (r'/admin', AdminHandler),
    (r'/admin/facebook', FacebookHandler),
    (r'/admin/facebookKids', FacebookKidsHandler),
    (r'/admin/website', WebsiteGroupHandler),],
    debug = True)

