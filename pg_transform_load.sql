-- for PostgreSQL
--

-- There is no "IF EXISTS" in older versions of postgres
DROP TABLE entries;

CREATE TABLE  entries (
       id INTEGER PRIMARY KEY, 
       url TEXT, entry_date TIMESTAMP, 
       title TEXT, activity_type TEXT, felt TEXT, duration_time_seconds INTERVAL, 
       distance_in_miles NUMERIC(7,4), distance_in_km NUMERIC(7,4), 
       description TEXT, effort_outof_5 INTEGER, gear TEXT, weather TEXT, calories INTEGER, 
       pace_per_mile INTERVAL, pace_per_km INTERVAL
);

