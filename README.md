# Replication of Finer (2018)

UChicago published a [working paper](https://news.uchicago.edu/article/2018/03/06/nyc-taxi-ride-data-suggest-cozy-relationship-between-big-banks-and-fed "working paper") by David Andrew Finer on March 2018 that cleverly uses publicly available data (in spite of the fact unis spend millions on good proprietary datasets like from Factset/COMPUSTAT) to figure out if the Fed (through the NY Fed channel) is breaking the embargo to primary dealers or market makers. 

This repo is a log at my attempt to reproduce his findings, and learn how to explore medium datasets on self hosted hardware (aka no BigQuery). If I successfully reproduce his results I may or may not find other interesting things from the TLC dataset that may counter his findings.

Prerequisites (or at least this is my current stack):
- Windows 10 with WSL (Windows Subsystem for Linux)
- Anaconda 3 using Python 3.6 (psycopg2,pandas,scipy)
- PostgreSQL 9.6 on the same machine



#### 1. Configuring database environment
I am in the process of using this extremely popular [repo](https://github.com/toddwschneider/nyc-taxi-data "repo") to dump the TLC data into my db and have rewritten several bash files in python. The only gnu tool you will need is `sed` to remove newlines/carriage returns from the .csvs so that psql can properly copy the files.




1. `psql create database "nyc-taxi-data"`

2. Download raw data to `data/`

`cd data/`
`wget -i ../raw_data_urls.txt`

3. Set up database and all tables/indexes using PostGIS

open up an sql client and run `create_nyc_taxi_schema.sql`

import the taxi codes (make sure you added your postgres bin folder to PATH) and use powershell to correctly pipe the inputs. Thanks to @tableflip for arguments help https://github.com/tableflip/how-to/issues/19

`shp2pgsql -s 2263:4326 taxi_zones/taxi_zones.shp taxi_zones | psql -d nyc-taxi-data -U <username>`

run

`CREATE INDEX index_taxi_zones_on_geom ON taxi_zones USING gist (geom);
CREATE INDEX index_taxi_zones_on_locationid ON taxi_zones (locationid);
VACUUM ANALYZE taxi_zones;`

repeat for newark airport

`shp2pgsql -s 2263:4326 .\nyct2010_15b\nyct2010.shp nyct2010 | psql -d nyc-taxi-data  -U <username>`

run `add_newark_airport.sql`

`CREATE INDEX index_nyct_on_geom ON nyct2010 USING gist (geom);
CREATE INDEX index_nyct_on_ntacode ON nyct2010 (ntacode);
VACUUM ANALYZE nyct2010;`


run `add_tract_to_zone_mapping.sql`

run in psql
`\COPY fhv_bases FROM "filepath/data/fhv_bases.csv" WITH CSV HEADER;

\COPY central_park_weather_observations (station_id, station_name, date, average_wind_speed, precipitation, snowfall, snow_depth, max_temperature, min_temperature) FROM 'C:\Users\Carlos\Documents\GitHub\tlc-nyfed\data\central_park_weather.csv' WITH CSV HEADER;

UPDATE central_park_weather_observations SET average_wind_speed = NULL WHERE average_wind_speed = -9999;`

4. import raw data and map to census tracts 

This is divided by green and yellow taxis. Open up WSL and cd to the data directory to remove carriage returns and newlines since psql uses binary to read files.

For green and yellow taxis run these two commands:

`sed -i $'s/\r$//' green*.csv ; sed  -i '/^$/d' green*.csv`


`sed -i $'s/\r$//' green*.csv ; sed  -i '/^$/d' green*.csv`

then run `import_data.py`
