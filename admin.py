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
from models import admins_list

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
PAGE_SIZE = 5


class AdminHandler(webapp2.RequestHandler):
    """This is the handler to display the Admin membership form."""

    def get(self):
        """Displays the admin form for the ambassadors/admins."""
        template_context = {}
        get_spoogler_context(self.request, template_context)
        # Find the name of the admin that is logged in
        current_user = template_context['user']
        user_email = current_user.email()
        strip_at_index = user_email.find("@")
        template_context['user_name'] = user_email[0:strip_at_index]

        query = Spoogler.query()
        query = query.order(-Spoogler.date_created).order(Spoogler.full_name)
        template_context['query'] = query
        self.update(template_context)
        #logging.info(self.request.get('not_on_groups'))

    def post(self):
        # get context
        template_context = {}
        get_spoogler_context(self.request, template_context)

        # Build query
        query = Spoogler.query()
        query = query.order(-Spoogler.date_created).order(Spoogler.full_name)
        #logging.info(template_context['work_status'])

        # Apply filters
        template_context['query'] = self._apply_filters(query, template_context)

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


    def _apply_filters(self, query, template_context):
        spoogler_emails = []
        spoogler_fb_emails = []

        if template_context['show_only_active']:  # Show active members only
            query = query.filter(Spoogler.status == 1)

        # Filter by email list and social media options
        if template_context['email_lists'] == 1:  # Show a list of the primary emails
            # Apply filters if any of the social media options is selected
            query = AdminHandler._filter_by_social_media(query, template_context)
            for q in query:
                spoogler_emails.append(q.spoogler_email)
            template_context['emails_list'] = spoogler_emails
        if template_context['email_lists'] == 2:  # Show a list of the facebook emails
            # Apply filters if any of the social media options is selected
            query = AdminHandler._filter_by_social_media(query, template_context)
            for q in query:
                spoogler_fb_emails.append(q.spoogler_fb_email)
            template_context['fb_emails_list'] = spoogler_fb_emails

        # Filter only by social media options
        query = AdminHandler._filter_by_social_media(query, template_context)

        # Filter by full name
        if template_context["full_name"]:
            query = query.filter(Spoogler.full_name == template_context["full_name"])

        # Filter by primary email
        if template_context["spoogler_email"]:
            query = query.filter(Spoogler.spoogler_email == template_context["spoogler_email"])

        # Filter by facebook email
        if template_context["spoogler_fb_email"]:
            query = query.filter(Spoogler.spoogler_fb_email == template_context["spoogler_fb_email"])

        # Filter by Googler's full name
        if template_context["googler_full_name"]:
            query = query.filter(Spoogler.googler_full_name == template_context["googler_full_name"])

        # Filter by Googler's ldap
        if template_context["googler_ldap"]:
            query = query.filter(Spoogler.googler_ldap == template_context["googler_ldap"])

        # Filter by country of origin
        if template_context["spoogler_country"] != 0:
            query = query.filter(Spoogler.spoogler_country == template_context["spoogler_country"])

        # If the spoogler's country of origin is the U.S., filter by U.S. state
        if template_context["spoogler_us_state"] != 0:
            query = query.filter(Spoogler.spoogler_us_state == template_context["spoogler_us_state"])

        # Filter by work status
        if template_context["work_status"] != 0:
            query = query.filter(Spoogler.work_status == template_context["work_status"])

        # Filter by english proficiency
        if template_context["english_proficiency"] != 0:
            query = query.filter(Spoogler.english_proficiency == template_context["english_proficiency"])

        # Filter by native language
        if template_context['native_lang'] != 0:
            query = query.filter(Spoogler.native_lang == template_context['native_lang'])

        # Filter by address
        if template_context['address'] != 0:
            query = query.filter(Spoogler.address == template_context['address'])

        # Filter by time living in the Bay Area
        if template_context["time_in_area"] != 0:
            query = query.filter(Spoogler.time_in_area == template_context["time_in_area"])

        # Filter by other local forms of support
        if template_context["support_others"]:
            support_groups = template_context["support_others"]
            for index in range(0, len(support_groups)):
                query = query.filter(Spoogler.support_others == support_groups[index])

        # Filter if spoogler is a parent and/or children ages
        is_parent_option = template_context["spoogler_is_parent"]
        if is_parent_option != 0:
            query = query.filter(Spoogler.spoogler_is_parent == is_parent_option)
            if is_parent_option == 1:
                if template_context["children_ages"]:
                    children = template_context["children_ages"]
                    for index in range(0, len(children)):
                        query = query.filter(Spoogler.children_ages == children[index])

        # Filter if Spoogler requested to join the FB KidsZone group or not
        join_FBKZ = template_context["kidszone_invite"]
        if join_FBKZ != 0:
            KZ_option = (join_FBKZ == 1)
            query = query.filter(Spoogler.kidszone_invite == KZ_option)

        return query

    @classmethod
    def _filter_by_social_media(cls, query, template_context):
        """
        Applies filters if any of the social media options is selected.
        :rtype: query object
        """
        if template_context['not_on_groups'] == 0:  # Clear social media options
            pass
        # Filter if the option "Not added to Google groups" is selected
        if template_context['not_on_groups'] == 1:
            query = query.filter(Spoogler.on_google_group == False)
        # Filter if the option "Not added to Facebook" is selected
        if template_context['not_on_groups'] == 2:
            query = query.filter(Spoogler.on_facebook == False)
        # Filter if the option "Not added to Facebook KidsZone" is selected
        # Only show emails of those who requested to join Facebook KidsZone
        if template_context['not_on_groups'] == 3:
            query = query.filter(Spoogler.kidszone_invite == True)
            query = query.filter(Spoogler.on_fb_kids == False)
        return query


# Handlers for AJAX requests


class GoogleGroupHandler(webapp2.RequestHandler):
    """ Handles the event where the administrator selects a checkbox
        when the Spoogler has been invited to the Google group to see
        the Spooglers official website."""
    def post(self):
        logging.info(self.request.get("googler_ldap"))
        logging.info(self.request.get("status"))
        current_user = users.get_current_user()
        googler_ldap = self.request.get("googler_ldap")
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap ==
                                      googler_ldap).fetch()
        spoogler = spoogler_qry[0]

        if self.request.get("status") == "true":
            spoogler.on_google_group = True
            spoogler.ambassador_gg = current_user.email()
            spoogler.ambassador_last = current_user.email()

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
        current_user = users.get_current_user()
        googler_ldap = self.request.get("googler_ldap")
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap ==
                                      googler_ldap).fetch()
        spoogler = spoogler_qry[0]

        if self.request.get("status") == "true":
            spoogler.on_facebook = True
            spoogler.ambassador_fb = current_user.email()
            spoogler.ambassador_last = current_user.email()

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
        current_user = users.get_current_user()
        spoogler_qry = Spoogler.query(Spoogler.googler_ldap ==
                                      googler_ldap).fetch()
        spoogler = spoogler_qry[0]

        if self.request.get("status") == "true":
            spoogler.on_fb_kids = True
            spoogler.ambassador_fbk = current_user.email()
            spoogler.ambassador_last = current_user.email()
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

