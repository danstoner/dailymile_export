-- for PostgreSQL, psql
--

--
-- Create some useful stored procedures for runners
--

CREATE OR REPLACE FUNCTION miles_to_km (miles NUMERIC) 
RETURNS NUMERIC AS $$
BEGIN
RETURN COALESCE((miles * 1.61)::NUMERIC(3,1),0);
END;
$$ LANGUAGE plpgsql;
-- SAMPLE miles_to_km
-- fitness=# select miles_to_km(3.1);
--  miles_to_km 
-- -------------
--          5.0
-- (1 row)


CREATE OR REPLACE FUNCTION km_to_miles (km NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
RETURN COALESCE((km * 0.62)::NUMERIC(3,1),0);
END;
$$ LANGUAGE plpgsql;
-- SAMPLE km_to_miles
-- fitness=# select km_to_miles(10);
--  km_to_miles 
-- -------------
--          6.2
-- (1 row)



--
-- Create the entries table
--

\echo Drop and Create table "entries"

-- There is no "IF EXISTS" in older versions of postgres
DROP TABLE entries;

CREATE TABLE  entries (
       id INTEGER PRIMARY KEY, 
       url TEXT, entry_date TIMESTAMP, 
       title TEXT, activity_type TEXT, felt TEXT, elapsed_time INTERVAL NOT NULL DEFAULT '59:59:59'::interval, 
       distance_in_miles NUMERIC(7,4) DEFAULT 0, distance_in_km NUMERIC(7,4) DEFAULT 0, 
       description TEXT, effort_outof_5 INTEGER, gear TEXT, weather TEXT, calories INTEGER, 
       pace_per_mile INTERVAL, pace_per_km INTERVAL
);


--
-- Transform and load the entries table from the raw import table 
--
\echo Inserting...
INSERT INTO entries (id, url, entry_date, title, activity_type, felt, description, effort_outof_5, gear, weather, calories)
SELECT id, url, entry_date, title, activity_type, felt, description, effort_outof_5, gear, weather, calories from imported_entries;

\echo Updating distance_in_km
UPDATE entries SET distance_in_km = miles_to_km (i.distance) FROM imported_entries i where i.distance_units = 'miles' AND entries.id = i.id;
UPDATE entries SET distance_in_km = i.distance FROM imported_entries i where i.distance_units = 'kilometers' AND entries.id = i.id;

\echo Updating distance_in_miles
UPDATE entries SET distance_in_miles = km_to_miles (i.distance) FROM imported_entries i where i.distance_units = 'kilometers' AND entries.id = i.id;
UPDATE entries SET distance_in_miles = i.distance FROM imported_entries i where i.distance_units = 'miles' AND entries.id = i.id;


\echo updating duration_time_seconds
UPDATE entries SET elapsed_time = COALESCE(i.duration_seconds * INTERVAL '1 second', '0 seconds'::INTERVAL) FROM imported_entries i WHERE entries.id = i.id;

\echo Setting pace_per_mile
UPDATE entries SET pace_per_mile = elapsed_time / distance_in_miles where distance_in_miles != 0;

\echo Setting pace_per_km
UPDATE entries SET pace_per_km = elapsed_time / distance_in_km where distance_in_km != 0;

-- TO DO  more thinking about NULL situations... where elapsed time is 0, distance is 0, pace is null or 0 or largest number for sorting?
-- NULL sorts at opposite end of ASC/DESC than 00:00:00 (zero elapsed time).

-- Sample:
-- fitness=# select id,title, elapsed_time, distance_in_miles, distance_in_km, pace_per_mile, pace_per_km 
-- from entries WHERE pace_per_mile between '5 minutes'::interval AND '7 minutes'::interval order by pace_per_mile limit 20; 
--     id    |                 title                  | elapsed_time | distance_in_miles | distance_in_km |  pace_per_mile  |   pace_per_km   
-- ----------+----------------------------------------+--------------+-------------------+----------------+-----------------+-----------------
--  35621592 | Track meet - 1500m race                | 00:04:48     |            0.9300 |         1.5000 | 00:05:09.677419 | 00:03:12
--  30113586 | Track Birthday Mile                    | 00:05:13     |            1.0000 |         1.6000 | 00:05:13        | 00:03:15.625
--  35646080 | Track - 1 Mile time trial              | 00:05:17     |            1.0000 |         1.6000 | 00:05:17        | 00:03:18.125
--  29211800 | Track meet 1500m                       | 00:04:46     |            0.9000 |         1.5000 | 00:05:17.777778 | 00:03:10.666667
--  24524049 | Time trial 1600m and 400m              | 00:06:45     |            1.2500 |         2.0000 | 00:05:24        | 00:03:22.5
--  34560219 | Florida Track Club - Shorter Mile race | 00:05:25     |            1.0000 |         1.6000 | 00:05:25        | 00:03:23.125
--  32994501 | Track meet 1500m                       | 00:04:53     |            0.9000 |         1.5000 | 00:05:25.555556 | 00:03:15.333333
--  36685940 | The Frank Shorter Mile race            | 00:05:27     |            1.0000 |         1.6000 | 00:05:27        | 00:03:24.375
--  19511537 | track time trials                      | 00:07:00     |            1.2500 |         2.0000 | 00:05:36        | 00:03:30
--  22225305 | Fallen Heroes 5k                       | 00:17:37     |            3.1000 |         5.0000 | 00:05:40.967742 | 00:03:31.4
--  31323702 | Gainesville Brewery Run 5k race        | 00:17:38     |            3.1000 |         5.0000 | 00:05:41.290323 | 00:03:31.6
--  29211805 | Track meet 3000m                       | 00:10:49     |            1.9000 |         3.0000 | 00:05:41.578947 | 00:03:36.333333
--  32994555 | Track meet 3000m                       | 00:10:56     |            1.9000 |         3.0000 | 00:05:45.263158 | 00:03:38.666667
--  33125817 | Our Town 5k race                       | 00:17:53     |            3.1000 |         5.0000 | 00:05:46.129032 | 00:03:34.6
--  32438909 | Flatwoods 5k race                      | 00:18:01     |            3.1000 |         5.0000 | 00:05:48.709677 | 00:03:36.2
--  21230618 | Race the Tortoise 5k                   | 00:18:07     |            3.1000 |         5.0000 | 00:05:50.645161 | 00:03:37.4
--  35010010 | Race the Tortoise 5k                   | 00:18:10     |            3.1000 |         5.0000 | 00:05:51.612903 | 00:03:38
--  28112999 | Flatwoods 5k race                      | 00:18:11     |            3.1000 |         5.0000 | 00:05:51.935484 | 00:03:38.2
--  35281689 | Hogtown 5k Beer Run                    | 00:18:47     |            3.2000 |         5.2000 | 00:05:52.1875   | 00:03:36.730769
--  23711830 | Melon Run 3 mile race                  | 00:17:41     |            3.0000 |         4.8000 | 00:05:53.666667 | 00:03:41.041667
-- (20 rows)
