import json
import requests
import time
import calendar
import logging
import csv
import codecs
import cStringIO
import traceback
import sys

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


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# BEGIN

# if we cannot open the output file might as well stop work here.
header = ["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description"]
outputfile = dm_user+"_dailymile_export."+str(time.time())+".csv"
with open(outputfile,"w") as f:
    writer = csv.writer(f)
    writer.writerow(header)



entry_dict = dict()

s = requests.Session()


###
### Will need to iterate through days since a start date using "since" and "until"
### rather than paging.
### Using the API "page" parameter does not guarantee getting every entry, 
### nor does it guarantee getting every entry only once.
###

# sample url for page 1 would be:
# https://api.dailymile.com/people/danstoner/entries.json?page=1
#api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

# to debug encoding issue on RIGHT SINGLE QUOTATION MARK
api_url_entries="http://api.dailymile.com/people/danstoner/entries.json?since=1284922400&until=1284999400"

logging.info("First API Request: " + api_url_entries)

r = s.get(api_url_entries)

while r.status_code == 200:
    r_json=r.json()
    for entry in r_json["entries"]:
        # Every JSON record seems to include "id", "url", and "at"
        id = entry["id"]
        # Assuming that paging through the API will not fetch a duplicate ID but
        # checking anyway because I seem to be able to pull an infinite number of pages,
        # far more than should exist in my entries.
        if id in entry_dict:
            logging.error("**ERROR** Duplicate ID: " + str(id))
            break
        entry_dict[id] = []
        entry_dict[id].append(str(id))
        entry_dict[id].append(str(entry.get("url")))
        entry_dict[id].append(str(entry.get("at")))
        # The JSON record does not always include every field
        try: entry_dict[id].append(str(entry["workout"].get("title")))
        except: entry_dict[id].append("")
        try: entry_dict[id].append(str(entry["workout"]["activity_type"]))
        except: entry_dict[id].append("")
        try: entry_dict[id].append(str(entry["workout"]["felt"]))
        except: entry_dict[id].append("")
        try: entry_dict[id].append(str(entry["workout"]["duration"]))
        except: entry_dict[id].append("")
        try: entry_dict[id].append(str(entry["workout"]["distance"]["value"]))
        except: entry_dict[id].append("")
        try: entry_dict[id].append(unicode(entry["workout"]["distance"]["units"]))
        except: entry_dict[id].append("")
        try: entry_dict[id].append(unicode(entry["message"]))
        except Exception, err:
            logging.error("encode exception: " + traceback.format_exc())
            entry_dict[id].append("")
        # The JSON record does not always include every field
        # try: entry_dict[id].append(entry["workout"].get("title"))
        # except: entry_dict[id].append("")
        # try: entry_dict[id].append(entry["workout"]["activity_type"])
        # except: entry_dict[id].append("")
        # try: entry_dict[id].append(entry["workout"]["felt"])
        # except: entry_dict[id].append("")
        # try: entry_dict[id].append(entry["workout"]["duration"])
        # except: entry_dict[id].append(None)
        # try: entry_dict[id].append(entry["workout"]["distance"]["value"])
        # except: entry_dict[id].append(None)
        # try: entry_dict[id].append(entry["workout"]["distance"]["units"])
        # except: entry_dict[id].append("")
        # try: entry_dict[id].append(unicode(entry["message"]))
        # except Exception, err:
        #     logging.error("encode exception: " + traceback.format_exc())
        #     entry_dict[id].append("")
    page+=1
    if page > 1:
        break
    api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)
    # give the API a break
    time.sleep(0.25)
    logging.info("Fetching: " + api_url_entries)
    r = s.get(api_url_entries)
    if r.status_code == 503:
        # probably hit the API requests per hour cap
        logging.error("Received HTTP 503. Please retry in: ____ seconds")
    if r.status_code == 404:
        # probably at the last page
        logging.error("Received HTTP 404 on " + api_url_entries)
    if r.status_code != 200:
        logging.error("Received unexpected HTTP status code " + r.status_code + " on " + api_url_entries)
        

with open(outputfile,"a") as f:
    writer = UnicodeWriter(f)
    for key in entry_dict:
        print entry_dict[key]
        try: writer.writerow(entry_dict[key])
        except Exception, err: 
            logging.error("Could not write: " + str(entry_dict[key]) + "," + traceback.format_exc())

#        for column in entry_dict[key]:
#            try: column = str(column).encode('utf-8')
#            except Exception, err: 
#                logging.error("Could not write: " + str(entry_dict[key]) + "," + traceback.format_exc())
#            print column
#        writer.writerow(entry_dict[key])

print entry_dict


### Current ERROR.  Probably copy and pasted this quote into dm. Tempted to edit the entry and fix it in the source data.

# ERROR:root:Could not write: [3368456, u'http://www.dailymile.com/entries/3368456', u'2010-09-19T22:34:39Z', '', '', '', None, None, '', u'Read "Running to the Top" by Arthur Lydiard. He would say that I do not yet have sufficient endurance base to start cranking out speed workouts. He has a nice rant about excessively supportive running shoes and orthotics (although he seems to be a supporter of heal striking) and says:  "If you could just attach a rubber sole to your foot, with nothing on the top, you\u2019d have the perfect running shoe."']
# Traceback (most recent call last):
#   File "dailymile_dump_json.py", line 210, in <module>
#     writer.writerow(entry_dict[key])
# UnicodeEncodeError: 'ascii' codec can't encode character u'\u2019' in position 369: ordinal not in range(128)
#
# API:
# http://api.dailymile.com/people/danstoner/entries.json?since=1284922400&until=1284999400
