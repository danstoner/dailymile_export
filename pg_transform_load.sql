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

-- Create some useful stored procedures for runners


CREATE OR REPLACE FUNCTION miles_to_km (miles NUMERIC(3,2))
RETURNS NUMERIC(3,2) AS $$
BEGIN
RETURN (miles * 1.61)::NUMERIC(3,1);
END;
$$ LANGUAGE plpgsql;
-- SAMPLE miles_to_km
-- fitness=# select miles_to_km(3.1);
--  miles_to_km 
-- -------------
--          5.0
-- (1 row)


CREATE OR REPLACE FUNCTION km_to_miles (km NUMERIC(3,2))
RETURNS NUMERIC(3,2) AS $$
BEGIN
RETURN (km * 0.62)::NUMERIC(3,1);
END;
$$ LANGUAGE plpgsql;
-- SAMPLE km_to_miles
-- fitness=# select km_to_miles(10);
--  km_to_miles 
-- -------------
--          6.2
-- (1 row)


