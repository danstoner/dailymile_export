import json
import requests
import datetime


dm_user="danstoner"

# start date is 2010-01-01  (january 1, 2010)
start_date = (2010,1,1).datetime

print start_date

exit

# API needs unix time seconds since the epoch
# See:
# https://www.dailymile.com/forums/bugs-and-support/topics/11340-api-question-about-getting-events-since-certain-date
date_since="1262304000"



api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json"

