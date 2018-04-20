dailymile_export
================

Export entries from dailymile using the API.

http://www.dailymile.com/api/documentation


The python script dailymile_export_to_tsv.py is the preferred and fully-functional edition of the software. The output format is tab-delimited file (.tsv).

The perl 5 script dailymile_export_to_csv.pl is less functional. The output format is csv-delimited file (.csv).

[Releases](https://github.com/danstoner/dailymile_export/releases/latest) are considered stable. 

The master branch may include experimental and broken features.


## Synopsis

### Python

```
$ python dailymile_export_to_tsv.py --help
usage: dailymile_export_to_tsv.py [-h] [-d] [-e] [-g] [-m MAXPAGES] [-w]
                                  USERNAME

Script to download entries from the dailymile API for a particular user into a
tab-delimited file.

positional arguments:
  USERNAME              The dailymile.com username of the account to export.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug level logging.
  -e, --extended        Retrieve extended info for each entry. Extended gear
                        includes Effort, Gear, Weather, and Calories. This
                        will SIGNIFICANTLY impact performance since every
                        single entry will require an additional web request
                        (extended data is not available via the API). Posts
                        must not be set to private in dailymile.
  -g, --gpx             Download the .GPX track for each entry.
  -m MAXPAGES, --maxpages MAXPAGES
                        Maximum number of API requests to make (to limit http
                        requests during testing)
  -w, --disablewarnings
                        Disable urllib3 warnings.

```

Sample test fetching only 2 pages of entries and included extended info:

```
$ $ python dailymile_export_to_tsv.py -e -m 2 danstoner
INFO:root:Max Pages = 2
INFO:root:First API Request: http://api.dailymile.com/people/danstoner/entries.json?page=1
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35671975/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35667222/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35664020/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35646080/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35646020/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35641287/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35634952/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35625017/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35621599/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35621592/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35621557/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35610449/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35599226/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35594410/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35587204/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35579619/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35574810/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35567753/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35559001/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35558933/workout_data
INFO:root:Fetching: http://api.dailymile.com/people/danstoner/entries.json?page=2
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35542790/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35538945/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35525964/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35517561/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35517519/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35512945/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35506318/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35500410/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35496586/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35486611/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35478421/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35478396/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35473418/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35461079/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35454399/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35448963/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35433177/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35433161/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35428708/workout_data
INFO:root:Fetching extended info from http://www.dailymile.com/people/danstoner/entries/35428676/workout_data
WARNING:root:Stopped processing. Hit maxpages limit. Use -m to set a larger value.
INFO:root:Total number of entries: 40
INFO:root:Writing to output file: danstoner_dailymile_export_py.20160618202709.51.tsv
```

Sample from the output file:

```
$ head -n 10 danstoner_dailymile_export_py.20160618202709.51.tsv
id     url   timestamp	title	activity_type	felt	duration_seconds	distance	distance_units	description effort_outof_5 gear weather calories
35428676     http://www.dailymile.com/entries/35428676	2016-05-09T17:44:33Z	campus		Running		alright	    1500	   2.5	miles	 2 VFF KSO EVO  314
35428708     http://www.dailymile.com/entries/35428708	2016-05-09T17:49:24Z	Stadium workout	Running		alright	    1200	   1	miles	 Abbreviated RMC style stadium workout. 3   251
35433161     http://www.dailymile.com/entries/35433161	2016-05-10T11:31:42Z	warmup and down	Running		alright	    3000	   5.45	miles	 Had some odd pains in my right foot at first. Legs sore from yesterday's workout. 1 Altra Samson  628
35433177     http://www.dailymile.com/entries/35433177	2016-05-10T11:34:27Z	Track - 9 x 300m alternating pace	    Running	   alright	 862 2.15 miles	    Track - 9 x 300m alternating pace between 3k and 1 mile pace. Short 100m jog recovery. 300m splits: 65, 58, 61, 56, 61, 55, 58, 53, 57 4 Altra Samson  175
35448963     http://www.dailymile.com/entries/35448963	2016-05-12T18:20:25Z	noonday warm run on campus   Running	    alright	   3047		 6.8 miles	    Perceived effort was high due to the noonday heat. Last 3 miles at just over 7 minute per mile pace.    3	VFF KSO EVO sunny   628
35454399     http://www.dailymile.com/entries/35454399	2016-05-13T16:01:55Z	Long on Hawthorne Trail	     Running	    blah	   6960		 13.1		    miles     Turned into a real slog fest.	 3     Altra Instinct 1.5 black	 hot sunny    1457
35461079     http://www.dailymile.com/entries/35461079	2016-05-14T21:20:19Z	Bacon Strip 11	  Running    alright	    5520	   11.18	 miles		    Hot and hilly in the late afternoon sun.	 3     Merrell Bare Access	     1155
35473418     http://www.dailymile.com/entries/35473418	2016-05-16T18:20:14Z	hill sprints	  Running    alright	    3420	   4.75		 miles		    10 x hill sprints after easy run	2	 VFF SeeYa LS  	    716
35478396     http://www.dailymile.com/entries/35478396	2016-05-17T14:39:49Z	warm up and down  Running    alright	    1200	   1.85		 miles		       2 Altra Samson 	    251
```

Full samples are available in the "output_files" directory of the project.


### Perl

```
$ perl dailymile_export_to_csv.pl --help

Description:

  Script to download entries from the dailymile API for a particular user into a CSV.

Usage: dailymile_export_to_tsv.pl [OPTIONS] <PARAMETERS>

  Parameters:
    --help, -h         Display this usage help.
    --username, -u USERNAME
                       The dailymile.com username to export (Required).
  Options:
    --debug, -d        Enable debug level output.
    --gear, -g         Enable download of gear info (not yet available)
    --maxpages, -m MAX
                       Maximum number of pages to fetch (to limit http requests during testing)
```

## Why write my own exporter?  

The built-in export feature of dailymile is abysmal.

The dailymile website's export only includes a small number of the available data fields 
(date,activity_type,distance,time,felt,elevation_gain). I spent a lot of time over
the years using dailymile as my serious runner training log. I want to be able to get
my data out (and be able to analyze it with my own tools, etc.).


## Feedback?  

Feel free to submit feedback using github Issues feature.
