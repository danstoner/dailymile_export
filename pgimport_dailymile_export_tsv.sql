# for PostgreSQL
# 
# DROP DATABASE IF EXISTS fitness;
# CREATE DATABASE fitness;
# \c fitness

# This begins the parts that are probably safe to run over and over as an ETL process

# no "IF EXISTS" in older versions of postgres
DROP TABLE imported_entries;


# postgres is awesome. We can be a little better about our column definitions than importing everything as text.
# posgres "does the right thing" with the import (via the COPY command)

# header = ["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description","effort_outof_5","gear","weather","calories"]
CREATE table imported_entries (id integer primary key, url text, entry_date timestamp, title text, activity_type text, felt text, duration_seconds integer, distance NUMERIC(7,4), distance_units text, description text, effort_outof_5 integer, gear text, weather text, calories integer);

# Note that a common issue with importing into postgresql has to do with
# file path / location and file permissions.
# I place the .tsv export file in /tmp before trying to load it into the db.

COPY imported_entries FROM '/tmp/danstoner_dailymile_export.tsv' WITH DELIMITER AS '\t' CSV HEADER;

## Alternative command using the postgresql \COPY command. Note there is no semicolon for \ commands.
##
## \COPY imported_entries FROM '/tmp/danstoner_dailymile_export.tsv' WITH DELIMITER AS '\t' CSV HEADER