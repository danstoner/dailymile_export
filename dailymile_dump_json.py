import json
import requests
import time
import calendar
import logging
import csv


# CONFIGURABLES

#TODO convert these to runtime parameters

# dailymile user name
dm_user="danstoner"

# Earliest date entry to fetch in format YYYY-MM-DD
## not yet using this...
#### start_date = "2010-01-01"


# log everything for now
logging.basicConfig(level=logging.DEBUG)


# API needs unix time aka ticks since the epoch
# See:
#  http://www.dailymile.com/api/documentation
#  http://www.unixtimestamp.com/
# Example: January 1, 2010 or 2010-01-01 would become "1262304000"
# 1262304000 01/01/2010 @ 12:00am (UTC)
# 1293840000 01/01/2011 @ 12:00am (UTC)
# 1325376000 01/01/2012 @ 12:00am (UTC)
# 1356998400 01/01/2013 @ 12:00am (UTC)
# 1388534400 01/01/2014 @ 12:00am (UTC)
# 1420070400 01/01/2015 @ 12:00am (UTC)

#### date_since = str(calendar.timegm(time.strptime(start_date,"%Y-%m-%d")))

# At some point will probably need to fetch by year due to the number of
# workouts / connections required to get all of the data.
# Until then, we will just start at page 1 and keep paging until there
# are no more pages. This is actually reasonable for a "full export" anyway.
#
# dailymile currently caps at 1500 requests per hour.

# start at page 1 and go until we run out of data
page = 1


###### API fields

# Sample API request and response
# $ curl -s  "https://api.dailymile.com/people/danstoner/entries.json?since=1420934400&until=1421020800" | json_pp
# {
#    "entries" : [
#       {
#          "url" : "http://www.dailymile.com/entries/31577777",
#          "at" : "2015-01-11T17:56:10Z",
#          "location" : {
#             "name" : "Gainesville, FL"
#          },
#          "comments" : [],
#          "message" : "First run in Inov-8 TrailRoc 235. Great shoes! Good protection, no cushion. Upper is snug to the foot without being tight. No blisters or rubbing. Ran parking lot to parking lot with 2 x Conquistador in the middle. Nice cool day. Trails were in good shape day after Tour de Felasco MTB and I mostly had them to myself. Forgot to charge my phone last night so I'm guessing at pace/distance. Meant to eat something mid-run but I forgot that, too. This caps off a 60 mile week.",
#          "workout" : {
#             "title" : "Hilly San Felasco Trails",
#             "activity_type" : "Running",
#             "distance" : {
#                "units" : "miles",
#                "value" : 24
#             },
#             "duration" : 14400,
#             "felt" : "good"
#          },
#          "user" : {
#             "username" : "danstoner",
#             "photo_url" : "https://dnetd3r67cewl.cloudfront.net/unsafe/48x48/https://d2d6zexjsynj7u.cloudfront.net/pictures/users/93956/1418935415.jpg",
#             "url" : "http://www.dailymile.com/people/danstoner",
#             "display_name" : "Dan S."
#          },
#          "id" : 31577777,
#          "likes" : []
#       }
#    ]
# }



# These are the fields that I want out of the api
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




# BEGIN

entry_dict = dict()

s = requests.Session()

# sample url for page 1 would be:
# https://api.dailymile.com/people/danstoner/entries.json?page=1
api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

#r = requests.get(api_url_entries)

logging.info("First API Request: " + api_url_entries)

r = s.get(api_url_entries)

while r.status_code == 200:
    r_json=r.json()
    for entry in r_json["entries"]:
        row = list(entry_dict[entry["id"]])
        entry_dict[entry["id"]] = row.insert
#        print r_json["id"]
#        for each in r.json()["entries"]:
#            print each["id"]
    page+=1
    if page > 1:    # stop after 5 pages for testing purposes
        break
    api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)
    # give the API a break
    time.sleep(0.25)
    logging.info("Fetching: " + api_url_entries)
    if r.status_code == 503:
        # probably hit the API requests per hour cap
        logging.error("Received HTTP 503. Please retry in: ____ seconds")
    if r.status_code == 404:
        # probably at the last page
        logging.error("Received HTTP 404 on " + api_url_entries)
    if r.status_code != 200:
        logging.error("Received unexpected HTTP status code " + r.status_code + " on " + api_url_entries)

print entry_dict
