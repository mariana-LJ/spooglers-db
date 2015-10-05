import sys
import csv
import re
import getpass

sys.path.append('/home/mlj/09_Python_Spooglers_DB/google_appengine')
sys.path.append('/home/mlj/09_Python_Spooglers_DB/google_appengine/lib/yaml/lib')
sys.path.append('/home/mlj/09_Python_Spooglers_DB/google_appengine/lib/fancy_urllib')

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.api import datastore_errors
import models

APP_ID = 's~baspooglers'
REMOTE_API_PATH = '/_ah/remote_api'
ADDRESS = 'baspooglers.appspot.com'

def auth_func():
    email_address = raw_input('Email address: ')
    password = getpass.getpass('Password: ')
    return email_address, password

def init_remote_api(app_id=APP_ID, path=REMOTE_API_PATH, address=ADDRESS):
    remote_api_stub.ConfigureRemoteApi(app_id, path, auth_func, address)
    remote_api_stub.MaybeInvokeAuthentication()

init_remote_api()
filename = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
with open(filename, 'rb') as csvfile:
    lines = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for i, line in enumerate(lines):
        if i < start or i >= end:
            continue
        # Parse all fields.
        full_name = line['Your name'].strip()
        if not full_name:
            print "Skipping no full_name, line: ", i+1 # header is line 1
            continue

        spoogler_email = line['Your email address'].strip()
        if not spoogler_email:
            print "Skipping no spoogler_email, line: ", i+1 # header is line 1
            continue

        googler_ldap = line['Your partner\'s @google.com address'].strip()
        if not googler_ldap:
            print "Skipping no googler_ldap, line: ", i+1 # header is line 1
            continue
        else:
            parts = re.split('@|\s', googler_ldap)
            if len(parts) == 1:
                googler_ldap = googler_ldap
            elif len(parts) == 2:
                googler_ldap = parts[0]
            else:
                print "Invalid googler email: ", googler_ldap, " line: ", i+1
                continue

        english_proficiency = line['What is your English language level?'].strip()
        if english_proficiency:
            option = [e[0] for e in models.proficiency_list if e[1] == english_proficiency]
            if option:
                english_proficiency = option[0]
            else:
                print "Unknown english proficiency: ", english_proficiency, " line:", i+1
                english_proficiency = 0
        else:
            english_proficiency = 0

        options = line['What type of events would you be interested in attending?'].strip()
        event_types = [e[0] for e in models.event_type_list if options.find(e[1]) != -1]

        spoogler = models.Spoogler.query(models.Spoogler.googler_ldap == googler_ldap).fetch()

        if len(spoogler) > 1:
            print "Duplicated record, line: ", i+1
            continue

        if spoogler:
            spoogler = spoogler[0]
        else:
            # Create Spoogler.
            spoogler = models.Spoogler()

        # Update values
        spoogler.full_name = full_name
        spoogler.spoogler_email = spoogler_email
        #spoogler_fb_email = template_context['spoogler_fb_email']
        #googler_full_name = template_context['googler_full_name']
        spoogler.googler_ldap = googler_ldap
        #spoogler_country = template_context['spoogler_country']
        #work_status = template_context['work_status']
        spoogler.english_proficiency = english_proficiency
        #native_lang = template_context['native_lang']
        #address = template_context['address']
        #other_address = template_context['other_address']
        #time_in_area = template_context['time_in_area']
        #spoogler_relo = template_context['spoogler_relo']
        #transportation = template_context['transportation']
        #side_driving = template_context['side_driving']
        #events_size = template_context['events_size']
        spoogler.event_types = event_types
        #event_types_other = template_context['event_types_other']
        #support_types = template_context['support_types']
        #support_types_other = template_context['support_types_other']
        #support_others = template_context['support_others']
        #support_others_other = template_context['support_others_other']
        #children_ages = template_context['children_ages']
        spoogler.migrated = True
        spoogler.test = False
        spoogler.status = 1
        spoogler.token = 0

        # An entity is persisted in the Datastore:
        try:
            spoogler.put()
            print "Record inserted: ", i, " line : ", i+1
        except datastore_errors.TransactionFailedError:
            print "Insert error, line: ", i+1

