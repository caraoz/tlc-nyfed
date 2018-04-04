# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 21:28:55 2018

@author: Carlos
"""

import re
import psycopg2
import glob
import time

try:
    conn = psycopg2.connect(dbname='nyc-taxi-data',host='localhost',user='postgres',password='root')
    conn.autocommit = True
except:
    print('die')
cur = conn.cursor()


year_month_regex="tripdata_([0-9]{4})-([0-9]{2})"
green_schema_pre_2015="(vendor_id,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,rate_code_id,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,total_amount,payment_type,trip_type,junk1,junk2)"

green_schema_2015_h1="(vendor_id,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,rate_code_id,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,improvement_surcharge,total_amount,payment_type,trip_type,junk1,junk2)"

green_schema_2015_h2_2016_h1="(vendor_id,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,rate_code_id,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,improvement_surcharge,total_amount,payment_type,trip_type)"

green_schema_2016_h2="(vendor_id,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,rate_code_id,pickup_location_id,dropoff_location_id,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,improvement_surcharge,total_amount,payment_type,trip_type,junk1,junk2)"

green_schema_2017_h1="(vendor_id,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,rate_code_id,pickup_location_id,dropoff_location_id,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,improvement_surcharge,total_amount,payment_type,trip_type)"

yellow_schema_pre_2015="(vendor_id,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,rate_code_id,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,total_amount)"

yellow_schema_2015_2016_h1="(vendor_id,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,rate_code_id,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount)"

yellow_schema_2016_h2="(vendor_id,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,rate_code_id,store_and_fwd_flag,pickup_location_id,dropoff_location_id,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,junk1,junk2)"

yellow_schema_2017_h1="(vendor_id,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,rate_code_id,store_and_fwd_flag,pickup_location_id,dropoff_location_id,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount)"

for filename in glob.glob('data/green*'):
    start = time.time()
    #print(filename)
    p = re.compile(year_month_regex)
    year = int(p.search(filename).group(1))
    month = int(p.search(filename).group(2))
    if year < 2015:
        schema = green_schema_pre_2015
    elif (year == 2015) and (month < 7):
        schema = green_schema_2015_h1
    elif (year == 2015) or ((year == 2016) and (month < 7)):
        schema = green_schema_2015_h2_2016_h1
    elif (year == 2016) or (month > 6):
        schema = green_schema_2016_h2
    else:
        schema = green_schema_2017_h1
    print(schema)
    
    filename = filename.replace('\\','/')
    print('start load time for',filename)
    filepath = filename
    
# =============================================================================
#     cur.execute(""" COPY green_tripdata_staging"""+schema+""" FROM 'E:/datasets/NYCYellowCabData/"""+filepath+"""' CSV HEADER """  )
#     print('elapsed',str(time.time()-start))
#     cur.execute(open('populate_green_trips.sql').read())
#     print('elapsed',str(time.time()-start))
# =============================================================================
