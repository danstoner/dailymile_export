dailymile_export
================

Export entries from dailymile using the API.

http://www.dailymile.com/api/documentation


The python script dailymile_export_to_tsv.py is functional and provides export to tab-delimited file (.tsv).

## Synopsis

```
$ python dailymile_export_to_tsv.py --help
usage: dailymile_export_to_tsv.py [-h] [-d] [-g] username

Script to download entries from the dailymile API for a particular user into a
tab-delimited file.

positional arguments:
  username     The dailymile.com username of the account to export.

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Enable debug level logging.
  -g, --gear   Retrieve gear data also.   [not yet implemented]
```


## Why write my own exporter?  

The built-in export feature of dailymile is abysmal.

The dailymile website export only includes a small number of the available data fields 
(date,activity_type,distance,time,felt,elevation_gain). I have spent a lot of time over
the years using dailymile as my serious runner training log. I want to be able to get
my data out (and be able to analyze it with my own tools, etc.).

## Future

I am writing versions of the script in other languages for personal learning and comparison.

I hope to export the gear information (so I can track shoe mileage) which isn't even available in the API.

Maybe eventually I will include additional fields such as tags and weather.

## Feedback?  

Feel free to submit feedback using github Issues feature.
