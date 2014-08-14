import json
import requests
import time
import calendar


# CONFIGURABLES
 
# dailymile user name
dm_user="danstoner"

## Pretty sure that the "since" parameter does not actually work in the API. I could not get 
## unix timestamp to affect the results of the API calls in any way.
# Earliest date entry to fetch in format YYYY-MM-DD
start_date = "2012-01-01"


# CODE

# API needs unix time aka ticks since the epoch
# See:
#  https://www.dailymile.com/forums/bugs-and-support/topics/11340-api-question-about-getting-events-since-certain-date
#  http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
# Example: January 1, 2010 or 2010-01-01 would become "1262304000"
date_since = str(calendar.timegm(time.strptime(start_date,"%Y-%m-%d")))


exit

# Will just need to page through every single entry starting with page 1 until there
# are no more pages.

#api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?since=" + date_since


# start at page 1 and go until we stop getting HTTP ok

page = 1

s = requests.Session()

api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

#r = requests.get(api_url_entries)
r = s.get(api_url_entries)

if r.status_code != 200:
    print "Did not get HTTP 200! Exiting."
    exit
else:
    for each in r.json()["entries"]:
        print each["id"]


