try:
    import argparse
    from bs4 import BeautifulSoup
    import json
    import logging
    import codecs
    import cStringIO
    import csv
    import requests
    import sys
    import time
    import traceback
except ImportError, e:
    print "IMPORT ERROR: %s" % e
    raise SystemExit

argparser = argparse.ArgumentParser(description='Script to download entries from the dailymile API for a particular user into a tab-delimited file.')
argparser.add_argument("USERNAME", help="The dailymile.com username of the account to export.")
argparser.add_argument("-d", "--debug", action="store_true", help="Enable debug level logging.")
argparser.add_argument("-e", "--extended", action="store_true", help="Retrieve extended info for each entry. This includes gear, effort, weather,  and calories. Note that this will greatly impact performance since every single entry will require a web request (gear data is not available via the API). Posts must not be set to private in dailymile.")
argparser.add_argument("-m", "--maxpages", type=int, help="Maximum number of API requests to make (to limit http requests during testing)")
args = argparser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

dm_user = args.USERNAME
extended_flag = args.extended
maxpages = args.maxpages

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
session = requests.Session()

def fetch_extended(entry_id):
    www_url_entry="https://www.dailymile.com/people/"+dm_user+"/entries/"+str(entry_id)+"/workout_data"
    print "fetching gear at "+www_url_entry
    soup=BeautifulSoup(session.get(www_url_entry))
    print (soup.prettify())
    

# if we cannot open the output file might as well stop work here.
# Using excel-tab as the output format (tab-delimited)
nowtimestring = time.strftime("%Y%m%d%H%M%S")
nowtimetime = str(time.time())  # just want some unique ms
ms = nowtimetime.rsplit('.')[ len(nowtimetime.rsplit('.')) - 1]
header = ["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description","gear","effort","weather","calories"]
outputfile = dm_user+"_dailymile_export_py."+ nowtimestring + "." + ms + ".tsv"
with open(outputfile,"w") as f:
    writer = UnicodeWriter(f,dialect='excel-tab')
    writer.writerow(header)

entry_dict = dict()


api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)

logging.info("First API Request: " + api_url_entries)

try: 
    r = requests.get(api_url_entries)
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
        if extended_flag:
            # do the soup here
            entry_dict[id].append("gear goes here")  # gear
            entry_dict[id].append("effort goes here")  # effort
            entry_dict[id].append("weather goes here")  # weather
            entry_dict[id].append("calories goes here")  # calories
            
            # try:
            #     entry_dict[id].append(fetch_gear(id));
            # except:
            #     entry_dict[id].append("")
            #     logging.error("Unable to append gear for id: "+str(id))
        else:
            # else we append empty columns
            entry_dict[id].append("")  # gear
            entry_dict[id].append("")  # effort
            entry_dict[id].append("")  # weather
            entry_dict[id].append("")  # calories
            
    page+=1
    if page > maxpages:
        logging.info("Pages is greater than maxpages.")
        break
    api_url_entries="https://api.dailymile.com/people/" + dm_user + "/entries.json?page=" + str(page)
    # give the API a break
    time.sleep(0.1)
    logging.info("Fetching: " + api_url_entries)
    try:
        r = requests.get(api_url_entries)
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
