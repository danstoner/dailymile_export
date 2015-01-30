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

# log everything for now
logging.basicConfig(level=logging.DEBUG)


# Earliest date entry to fetch in format YYYY-MM-DD
## not yet using this...
#### start_date = "2010-01-01"

#### date_since = str(calendar.timegm(time.strptime(start_date,"%Y-%m-%d")))

# At some point will probably need to fetch by year due to the number of
# workouts / connections required to get all of the data.
# Until then, we will just start at page 1 and keep paging until there
# are no more pages. This is actually reasonable for a "full export" anyway.
#

# start at page 1 and go until we run out of data
page = 1


# UnicodeWriter class taken straight out of python docs
# https://docs.python.org/2.7/library/csv.html#examples
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
# Using excel-tab as the output format (tab-delimited)
header = ["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description"]
outputfile = dm_user+"_dailymile_export."+str(time.time())+".tsv"
with open(outputfile,"w") as f:
    writer = UnicodeWriter(f,dialect='excel-tab')
    writer.writerow(header)

entry_dict = dict()

s = requests.Session()

api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

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
        # convert everything to string so CSV class can encode without error
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
        except UnicodeEncodeError, err:
            logging.error("encode exception: " + traceback.format_exc())
            entry_dict[id].append("")
        except: entry_dict[id].append("")
    page+=1
    if page > 20: # cut down number of page requests for testing
        break
    api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)
    # give the API a break
    time.sleep(0.1)
    logging.info("Fetching: " + api_url_entries)
    r = s.get(api_url_entries)
    if r.status_code == 503:
        # probably hit the API requests per hour cap, check Retry-After header (future work)
        logging.error("Received HTTP 503. Please retry in: ____ seconds")
    if r.status_code == 404:
        # probably at the last page
        logging.error("Received HTTP 404 on " + api_url_entries)
    if r.status_code != 200:
        logging.error("Received unexpected HTTP status code " + r.status_code + " on " + api_url_entries)

# The ids look like sequential numbers, sorting by id may go a long way towards getting the entries in chronological order
sorted_keys = sorted(entry_dict.keys())

# write the data to csv     
with open(outputfile,"a") as f:
    writer = UnicodeWriter(f,dialect='excel-tab')
    for key in sorted_keys:
        try: writer.writerow(entry_dict[key])
        except Exception, err: 
            logging.error("Could not write: " + str(entry_dict[key]) + "," + traceback.format_exc())
