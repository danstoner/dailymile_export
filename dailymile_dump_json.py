import json
import requests
import time
import calendar


# CONFIGURABLES
 
# dailymile user name
dm_user="danstoner"


# Earliest date entry to fetch in format YYYY-MM-DD
start_date = "2012-01-01"

# API needs unix time aka ticks since the epoch
# See:
#  http://www.dailymile.com/api/documentation
#  https://www.dailymile.com/forums/bugs-and-support/topics/11340-api-question-about-getting-events-since-certain-date
#  http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
# Example: January 1, 2010 or 2010-01-01 would become "1262304000"
date_since = str(calendar.timegm(time.strptime(start_date,"%Y-%m-%d")))

## Pretty sure that the "since" parameter does not actually work in the API. I could not get 
## unix timestamp to affect the results of the API calls in any way.  So instead, 
## will just page through every single entry starting with page 1 until there
## are no more pages. This is actually reasonable for a "full export" anyway (until we blow out 
#  some max requests limit... dailymile currently caps at 1500 requests per hour).

# start at page 1 and go until we stop getting HTTP ok
page = 1


###### API fields
# These are what we want out of the api
#
# id
# url
# at
# message
# workout
#   activity_type
#   distance
#     value
#     units
#   felt
#   duration
#   title
#
# workout: {
# activity_type: "Running",
# distance: {
# value: 3.8,
# units: "miles"
# },
# felt: "good",
# duration: 1620,
# title: "Track workout"
# }

# CODE

s = requests.Session()

# sample url for page 1 would be:
# https://api.dailymile.com/people/danstoner/entries.json?page=1
api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

#r = requests.get(api_url_entries)

while True:
    r = s.get(api_url_entries)
    if r.status_code != 200:
        print "Did not get HTTP 200! Exiting."
        break
    else:
        for each in r.json()["entries"]:
            print each["id"]
        page+=1
        api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)
        if page > 5:    # stop after 5 pages for testing purposes
            break


