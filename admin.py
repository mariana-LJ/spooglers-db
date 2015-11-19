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
        logging.info(self.request.get('not_on_groups'))

    def post(self):
        # get context
        template_context = {}
        get_spoogler_context(self.request, template_context)

        # build query
        query = Spoogler.query()
        if template_context['show_only_active']:
            query = query.filter(Spoogler.status == 1)
        if template_context['not_on_groups'] == 0:  # Clear social media options
            pass
        if template_context['not_on_groups'] == 1:  # Not added to Google groups
            query = query.filter(Spoogler.on_google_group == False)
        if template_context['not_on_groups'] == 2:  # Not added to Facebook
            query = query.filter(Spoogler.on_facebook == False)
        if template_context['not_on_groups'] == 3:  # Not added to Facebook KidsZone
            query = query.filter(Spoogler.on_fb_kids == False)
        if template_context['native_lang'] != 0:
            query = query.filter(Spoogler.native_lang == template_context['native_lang'])
        if template_context['address'] != 0:
            query = query.filter(Spoogler.address == template_context['address'])
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

# Handlers for AJAX requests


class GoogleGroupHandler(webapp2.RequestHandler):
    """ Handles the event where the administrator selects a checkbox
        when the Spoogler has been invited to the Google group to see
        the Spooglers official website."""
    def post(self):
        logging.info(self.request.get("googler_ldap"))
        logging.info(self.request.get("status"))
        ambassador = users.get_current_user()
        googler_ldap = self.request.get("googler_ldap")
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap ==
                                      googler_ldap).fetch()
        spoogler = spoogler_qry[0]

        if self.request.get("status") == "true":
            spoogler.on_google_group = True
            spoogler.ambassador = str(ambassador.nickname())

        try:
            spoogler.put()
            self.response.out.write(spoogler.full_name + 'was registered as part of the Google group.')
        except datastore_errors.TransactionFailedError:
            self.response.out.write('Error: please try again')


class FacebookHandler(webapp2.RequestHandler):
    """Handles the event where the administrator selects a checkbox
       when the Spoogler has been invited/added to the Facebook group.
    """

    def post(self):
        logging.info(self.request.get("googler_ldap"))
        logging.info(self.request.get("status"))
        ambassador = users.get_current_user()
        googler_ldap = self.request.get("googler_ldap")
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap ==
                                      googler_ldap).fetch()
        spoogler = spoogler_qry[0]

        if self.request.get("status") == "true":
            spoogler.on_facebook = True
            spoogler.ambassador = str(ambassador.nickname())

        try:
            spoogler.put()
            self.response.out.write(spoogler.full_name + ' was registered as part of the Facebook group.')
        except datastore_errors.TransactionFailedError:
            self.response.out.write('Error: please try again')


class FacebookKidsHandler(webapp2.RequestHandler):
    """ Handles the event where the administrator selects a checkbox
        when the Spoogler has been invited to the Facebook KidsZone group."""

    def post(self):
        logging.info(self.request.get("googler_ldap"))
        logging.info(self.request.get("status"))
        googler_ldap = self.request.get("googler_ldap")
        ambassador = users.get_current_user()
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap ==
                                      googler_ldap).fetch()
        spoogler = spoogler_qry[0]

        if self.request.get("status") == "true":
            spoogler.on_fb_kids = True
            spoogler.ambassador = str(ambassador.nickname())

        try:
            spoogler.put()
            self.response.out.write(spoogler.full_name + ' was registered as part of the Facebook KidsZone group.')
        except datastore_errors.TransactionFailedError:
            self.response.out.write('Error: please try again')



# pylint: disable = C0103

app = webapp2.WSGIApplication([
    (r'/admin', AdminHandler),
    (r'/admin/facebook', FacebookHandler),
    (r'/admin/fb_kids', FacebookKidsHandler),
    (r'/admin/google_group', GoogleGroupHandler),],
    debug = True)

