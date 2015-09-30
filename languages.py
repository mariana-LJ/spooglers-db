import csv
import re
import pprint

__author__ = 'bayareaspooglers.webmaster@gmail.com'

""" Short script to obtain the top ten languages spoken by the Bay Area Spooglers Group. """

world_languages = ['Akan', 'Amharic', 'Arabic', 'Assamese', 'Awadhi', 'Azerbaijani', 'Balochi', 'Belarusian', 'Bengali', 'Bhojpuri',
                   'Burmese', 'Cebuano', 'Chewa', 'Chhattisgarhi', 'Chittagonian', 'Czech', 'Deccan', 'Dhundhari', 'Dutch', 'Eastern Min',
                   'English', 'French', 'Fula', 'Gan Chinese', 'German', 'Greek', 'Gujarati', 'Haitian Creole', 'Hakka', 'Haryanvi', 'Hausa',
                   'Hiligaynon', 'Hindi', 'Hmong', 'Hungarian', 'Igbo', 'Ilocano', 'Italian', 'Japanese', 'Javanese', 'Jin', 'Kannada',
                   'Kazakh', 'Khmer', 'Kinyarwanda', 'Kirundi', 'Konkani', 'Korean', 'Kurdish', 'Madurese', 'Magahi', 'Maithili', 'Malagasy',
                   'Malay/Indonesian', 'Malayalam', 'Mandarin', 'Marathi', 'Marwari', 'Mossi', 'Nepali', 'Northern Min', 'Odia (Oriya)',
                   'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Saraiki',
                   'Serbo-Croatian', 'Shona', 'Sindhi', 'Sinhalese', 'Somali', 'Southern Min', 'Spanish', 'Sundanese', 'Swedish', 'Sylheti',
                   'Tagalog', 'Tamil', 'Telugu', 'Thai']
filename = '/home/mlj/Downloads/BAS Member Intake Form responses.csv'
spoogler_languages = {}
other_words = {}

with open(filename, 'rb') as csvfile:
    i = 0
    lines = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for line in lines:
        i += 1
        native_language = line['What, if any, other languages do you speak and at what level?'].strip()
        native_language = re.split('; |, |- |: |\n | ', native_language)
        for word in native_language:
            if word in world_languages:
                if word not in spoogler_languages.keys():
                    spoogler_languages[word] = 1
                else:
                    spoogler_languages[word] += 1
            else:
                if word not in other_words.keys():
                    other_words[word] = 1
                else:
                    other_words[word] += 1

top_ten_languages = []

for i in range(0, 10):
    max_val = 0
    for word in spoogler_languages:
        if spoogler_languages[word] > max_val:
            max_val = spoogler_languages[word]
            language = word
    top_ten_languages.append((language, max_val))
    spoogler_languages.pop(language, None)
    if language not in spoogler_languages.keys():
        continue
    else:
        print('error')
        break

pprint.pprint(top_ten_languages)
pprint.pprint(spoogler_languages)
