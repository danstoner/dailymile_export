
# DROP DATABASE IF EXISTS fitness;
# CREATE DATABASE fitness CHARACTER SET utf8 COLLATE utf8_general_ci;


# This begins the parts that are probably safe to run over and over as an ETL process

DROP TABLE IF EXISTS imported_entries;

CREATE TABLE imported_entries
(id INT PRIMARY KEY, url varchar(50), timestamp varchar(25), title varchar(256), activity_type varchar(25), 
felt varchar(25), duration_seconds INT, distance varchar(25), distance_units varchar(25), description varchar(2000));

LOAD DATA LOCAL INFILE 
'danstoner_dailymile_export.tsv' INTO TABLE imported_entries FIELDS TERMINATED BY '\t' IGNORE 1 LINES;