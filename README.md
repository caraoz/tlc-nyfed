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

import the taxi codes (make sure you added your postgres bin folder to PATH) and use powershell to correctly pipe the inputs

`shp2pgsql -s 2263:4326 taxi_zones/taxi_zones.shp taxizones | psql -d nyc-taxi-data -U <username>`

