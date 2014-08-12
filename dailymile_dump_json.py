import json
import requests
import time
import calendar

# CONFIGURABLES

# dailymile user name
dm_user="danstoner"

# earliest date entry to fetch in format YYYY-MM-DD
start_date = "2010-01-01"


# CODE

# API needs unix time aka ticks since the epoch
# See:
#  https://www.dailymile.com/forums/bugs-and-support/topics/11340-api-question-about-getting-events-since-certain-date
#  http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
# Example: January 1, 2010 or 2010-01-01 would become "1262304000"
date_since = str(calendar.timegm(time.strptime(start_date,"%Y-%m-%d")))


exit

api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?since=" + date_since

r = requests.get(api_url_entries)

# getting back restuls from API but this is not getting the "since 2010" part right.


if r.status_code != 200:
    print "Did not get HTTP 200! Exiting."
    exit
else:
    print r.content

