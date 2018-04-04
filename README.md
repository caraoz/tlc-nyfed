# Replication of Finer (2018)

UChicago published a [working paper](https://news.uchicago.edu/article/2018/03/06/nyc-taxi-ride-data-suggest-cozy-relationship-between-big-banks-and-fed "working paper") by David Andrew Finer on March 2018 that cleverly uses publicly available data (in spite of the fact unis spend millions on good proprietary datasets like from Factset/COMPUSTAT) to figure out if the Fed (through the NY Fed channel) is breaking the embargo to primary dealers or market makers. 

This repo is a log at my attempt to reproduce his findings, and learn how to explore medium datasets on self hosted hardware (aka no BigQuery). If I successfully reproduce his results I may or may not find other interesting things from the TLC dataset that may counter his findings.

Prerequisites (or at least this is my current stack):
- Windows 10 with WSL (Windows Subsystem for Linux)
- Anaconda 3 using Python 3.6 (psycopg2,pandas,scipy)
- PostgreSQL 9.6 on the same machine



#### 1. Configuring database environment
I am in the process of using this extremely popular [repo](https://github.com/toddwschneider/nyc-taxi-data "repo") to dump the TLC data into my db and have rewritten several bash files in python. The only gnu tool you will need is `sed` to remove newlines/carriage returns from the .csvs so that psql can properly copy the files.

**NOTE**: since `shp2pgsql ` does not want to work with windows or I messed up something, I can not invoke it from powershell and must use the gui tool provided. Since it was written badly the srid was set to 2263 instead of 4326.