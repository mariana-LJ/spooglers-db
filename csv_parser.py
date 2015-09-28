import sys
import csv
import  re
import getpass

sys.path.append('/home/acp/google_appengine')
sys.path.append('/home/acp/google_appengine/lib/yaml/lib')
sys.path.append('/home/acp/google_appengine/lib/fancy_urllib')

from google.appengine.ext.remote_api import remote_api_stub
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
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
spooglers = models.Spoogler.query()

for s in spooglers:
    print s.full_name

filename = sys.argv[1]

with open(filename, 'rb') as csvfile:
    i = 0
    lines = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for line in lines:
        i += 1
        full_name = line['Your name'].strip()
        spoogler_email = line['Your email address'].strip()
        googler_ldap = line['Your partner\'s @google.com address'].strip()
        english_proficiency = line['What is your English language level?'].strip()

        if not full_name:
            print "Skipping no full_name, line: ", i+1 # header is line 1
            continue

        if not spoogler_email:
            print "Skipping no spoogler_email, line: ", i+1 # header is line 1
            continue

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

        if english_proficiency:
            option = [e[0] for e in models.proficiency_list if e[1] == english_proficiency]
            if option:
                english_proficiency = option[0]
            else:
                print "Unknown english proficiency: ", english_proficiency, " line:", i+1
                english_proficiency = 0
        else:
            english_proficiency = 0

    print(i)
