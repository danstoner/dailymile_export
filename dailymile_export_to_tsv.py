try:
    import json
    import requests
    import time
    import logging
    import csv
    import codecs
    import cStringIO
    import traceback
    import sys
    import argparse
except ImportError, e:
    print "IMPORT ERROR: %s" % e
    raise SystemExit

argparser = argparse.ArgumentParser(description='Script to download entries from the dailymile API for a particular user into a tab-delimited file.')
argparser.add_argument("username", help="The dailymile.com username of the account to export.")
argparser.add_argument("-d", "--debug", action="store_true", help="Enable debug level logging.")
argparser.add_argument("-g", "--gear", action="store_true", help="Retrieve gear data also.")
args = argparser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

dm_user = args.username

if args.gear:
    logging.info("*** Gear data downloads not yet enabled in this script. ***")


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
nowtimestring = time.strftime("%Y%m%d%H%M%S")
nowtimetime = str(time.time())  # just want some unique ms
ms = nowtimetime.rsplit('.')[ len(nowtimetime.rsplit('.')) - 1]
header = ["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description"]
outputfile = dm_user+"_dailymile_export_py."+ nowtimestring + "." + ms + ".tsv"
with open(outputfile,"w") as f:
    writer = UnicodeWriter(f,dialect='excel-tab')
    writer.writerow(header)

entry_dict = dict()

s = requests.Session()

api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

logging.info("First API Request: " + api_url_entries)

try: 
    r = s.get(api_url_entries)
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    logging.error(e)
    raise SystemExit

r_json=r.json()

while (r.status_code == 200) and (r_json["entries"]):
    for entry in r_json["entries"]:
        # Every JSON record seems to include "id", "url", and "at"
        id = entry["id"]
        # Assuming that paging through the API will not fetch a duplicate ID but
        # checking anyway.
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
    api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)
    # give the API a break
    time.sleep(0.1)
    logging.info("Fetching: " + api_url_entries)
    try:
        r = s.get(api_url_entries)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if r.status_code == 503:
            logging.error("May have hit Requests per hour limit. Please retry later. Received: " + str(e))
            break
        else:
            logging.error("Error on GET request. Received: " + str(e))
            break
    r_json=r.json()

# The ids look like sequential numbers, sorting by id may go a long way towards getting the entries in chronological order
sorted_keys = sorted(entry_dict.keys())

logging.info("Total number of entries: "+str(len(sorted_keys)))
logging.info("Writing to output file: " + outputfile)

# write the data to csv     
with open(outputfile,"a") as f:
    writer = UnicodeWriter(f,dialect='excel-tab')
    for key in sorted_keys:
        try: writer.writerow(entry_dict[key])
        except Exception, err: 
            logging.error("Could not write: " + str(entry_dict[key]) + "," + traceback.format_exc())
