# -*- coding: utf-8 -*-
"""DataEngineeringFullETL.py

### Andrew deBerardinis

## Data import

## This is a dataset of every traffic collision report recorded by the San Diego Police Department from 2015 to present.
## https://data.sandiego.gov/datasets/police-collisions/
"""

## Import Statements
import pandas as pd
import numpy as np

## Read in csv
san_diego_accidents = pd.read_csv("https://seshat.datasd.org/pd/pd_collisions_datasd_v1.csv")

## Check to verify
print(san_diego_accidents)

"""## Data exploration

 

"""

'''
## Exploring data
print(san_diego_accidents.describe())
print("\n")
## Checking NA count
print(san_diego_accidents['address_sfx_primary'].isna().sum())
print(san_diego_accidents['hit_run_lvl'].isna().sum())
print(san_diego_accidents['veh_make'].isna().sum())

## Checking unique values and NA count in columns
print(san_diego_accidents['violation_type'].unique())
print(san_diego_accidents['veh_model'].isna().sum())
print(san_diego_accidents['person_role'].unique())
print(san_diego_accidents['person_role'].isna().sum())
'''

## Exploring vehicles that killed the most people during accidents
san_diego_accidents_by_veh_make = san_diego_accidents.groupby(san_diego_accidents['veh_make'], 
                                                              as_index=False).agg({'killed':['sum']})

## Change column names
san_diego_accidents_by_veh_make.columns = ['vehicle_make', 'total_killed']

## Sort vehicles by most killed
san_diego_accidents_by_veh_make.sort_values(by='total_killed', ascending=False).head()

## Exploring total killed by charge description
san_diego_accidents_by_charge = san_diego_accidents.groupby(san_diego_accidents['charge_desc'], 
                                                            as_index = False).agg({'killed':['count', 'sum']})

## Change column names
san_diego_accidents_by_charge.columns = ['charge_description', 'accident_count', 'total_killed']

print('\n')
print("Total killed in accidents recorded = " + str(san_diego_accidents_by_charge['total_killed'].sum()))
print('\n')


## Sorted to see which description had the most killed
san_diego_accidents_by_charge.sort_values(by='accident_count', ascending=False).head()

## Sorted to see which description had the most accidents
san_diego_accidents_by_charge.sort_values(by='total_killed', ascending=False).head()

"""
## Roadmap

The data is from data.sandiego.gov and consists of traffic collision reports recorded by the San Diego Police Department. 
I looked at all of the columns and wanted to take my data to figure out number of accidents, total injured and total killed 
in different types of accidents. I first need to remove NA values from columns explored in the above section. I also need 
to select the relevant columns like charge_desc, injured, killed. After that I can group by violation section and aggregate 
the counts and sums of columns. I need to make a new column with violation_ids corrseponding to violation_section. 
This is so I can create a table with descriptions for all violations corresponding to the violations that kill or injure 
anyone. I will create a table with violation information and its description. I will then create a table with accident count, 
total killed, and total injured for every violation section. Violation will be the primary key relating both tables. 
I will then have tables for finding accident numbers, total kills, and total injuries for every type of violation and a 
related table with descriptions of every violation section.

## Transforms

"""

## Check the shape
san_diego_accidents.shape

## Removing NA from colomn address_sfx_primary
san_diego_accidents = san_diego_accidents[san_diego_accidents['address_sfx_primary'].notna()]

## Check to see if correct number of rows was removed. Number of NA were found in data exploration
san_diego_accidents.shape

## Removing NA from colomn hit_run_lvl
san_diego_accidents = san_diego_accidents[san_diego_accidents['hit_run_lvl'].notna()]

## Removing NA from colomn veh_make
san_diego_accidents = san_diego_accidents[san_diego_accidents['veh_make'].notna()]

## Checking amount of rows with NA in column veh_model
## print(san_diego_accidents['veh_model'].isna().sum())

## Removing NA from colomn veh_model
san_diego_accidents = san_diego_accidents[san_diego_accidents['veh_model'].notna()]

## Verfying correct number of rows were removed
san_diego_accidents.shape

## Every colomn in san_diego_accidents
san_diego_accidents.columns

## Selecting only columns I need
san_diego_accidents = san_diego_accidents[['veh_make', 'police_beat', 'address_road_primary',
       'address_sfx_primary', 'violation_section', 'violation_type', 'charge_desc', 'injured', 'killed', 'hit_run_lvl']]

# I confirmed address_sfx_primary is not missing data. It is just not needed for certain address'
san_diego_accidents.head()
"""## Normalize data for loads
 
Break down the data into normalized tables then push to database. 

"""

## Add violation_id column in san_diego_accidents
san_diego_accidents['violation_id'] = pd.factorize(san_diego_accidents['violation_section'])[0].astype(str)

## print(san_diego_accidents.head())

## Group by violation_id with aggregations of count and sum of killed column and sum of injured column
violations_df = san_diego_accidents.groupby(san_diego_accidents['violation_id'], 
                                            as_index=False).agg({'killed':['count', 'sum'], 'injured':['sum']})
##  print(violations_df)

## Change column names
violations_df.columns = ['violation_id', 'number_of_accidents', 'total_killed', 'total_injured']

## Check df
print(violations_df)
print('\n')
print('\n')

## Select columns from san_diego_accidents and drop duplicates
violation_desc_df = san_diego_accidents[['violation_section', 'violation_type', 'charge_desc', 
                                         'violation_id']].drop_duplicates()

violation_desc_df.columns = ['violation_section', 'violation_type', 'charge_description', 'violation_id']

## Check df
print(violation_desc_df)
print('\n')
print('\n')

"""## Load to database

"""

import psycopg2

## Function to connect to my created AWS db
def get_conn_cur():
  conn = psycopg2.connect(
    host="ista322-final-project-db.cqrugokm56zq.us-east-2.rds.amazonaws.com",
    database="ista322_final_project_db",
    user="andrewdeb7",
    password="Nike_Elite7",
    port='5432')
  
  cur = conn.cursor()
  return(conn, cur)

# Run or old functions in case we want to check our data!

# run_query function
def run_query(query_string):

  conn, cur = get_conn_cur() # get connection and cursor

  cur.execute(query_string) # executing string as before

  my_data = cur.fetchall() # fetch query data as before

  # here we're extracting the 0th element for each item in cur.description
  colnames = [desc[0] for desc in cur.description]

  cur.close() # close
  conn.close() # close

  return(colnames, my_data) # return column names AND data

# Column name function for checking out what's in a table
def get_column_names(table_name): # arguement of table_name
  conn, cur = get_conn_cur() # get connection and cursor

  # Now select column names while inserting the table name into the WERE
  column_name_query =  """SELECT column_name FROM information_schema.columns
       WHERE table_name = '%s' """ %table_name

  cur.execute(column_name_query) # exectue
  my_data = cur.fetchall() # store

  cur.close() # close
  conn.close() # close

  return(my_data) # return

# Check table_names
def get_table_names():
  conn, cur = get_conn_cur() # get connection and cursor

  # query to get table names
  table_name_query = """SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public' """

  cur.execute(table_name_query) # execute
  my_data = cur.fetchall() # fetch results

  cur.close() #close cursor
  conn.close() # close connection

  return(my_data) # return your fetched results
  
# make sql_head function
def sql_head(table_name):
  conn, cur = get_conn_cur() # get connection and cursor

  # Now select column names while inserting the table name into the WERE
  head_query =  """SELECT * FROM %s LIMIT 5; """ %table_name

  cur.execute(head_query) # exectue
  colnames = [desc[0] for desc in cur.description] # get column names
  my_data = cur.fetchall() # store first five rows

  cur.close() # close
  conn.close() # close

  df = pd.DataFrame(data = my_data, columns = colnames) # make into df

  return(df) # return

## Connect to db
conn, cur = get_conn_cur()

## Check connection
## conn

## Create table in aws database
## Table already created
## Only needs to run before table is created
'''
sq = """CREATE TABLE violations (
          violation_id INTEGER PRIMARY KEY,
          number_of_accidents INTEGER NOT NULL, 
          total_killed INTEGER NOT NULL,
          total_injured INTEGER NOT NULL
          );"""
'''

## Execute query above
##cur.execute(sq)

## Commit query
##conn.commit()

## Check if table was added to database
## get_table_names()

# Use sql_head to check cases
## sql_head(table_name='violations')

## Get column names and datatypes from newly created table
conn, cur = get_conn_cur()
cur = conn.cursor()
uq = """SELECT column_name, data_type
          FROM information_schema.columns
          WHERE table_name = 'violations';"""
cur.execute(uq)
## print(cur.fetchall())
conn.close()

## For loop to get everything in violations_df
data_tups = [tuple(x) for x in violations_df.to_numpy()]

## Check values
## data_tups[2]

## Check query
iq = """INSERT INTO violations(violation_id,number_of_accidents,total_killed,total_injured) VALUES(%s, %s, %s, %s);"""
## iq

## Check query
## iq % data_tups[2]

## Upload to table in database
## Uploaded already
'''
conn, cur = get_conn_cur()
cur.executemany(iq, data_tups)
conn.commit()
conn.close()
'''

## Connect to db
conn, cur = get_conn_cur()

## Check connection
## conn

## Create second table in aws database
'''
tq = """CREATE TABLE violation_descriptions (
          violation_section varchar(225) NOT NULL,
          violation_type varchar(225) NOT NULL, 
          charge_description varchar(225) NOT NULL,
          violation_id INTEGER NOT NULL
          );"""
'''

## Execute query above
## cur.execute(tq)

## Commit query
## conn.commit()

## Check if table was added to database
## get_table_names()

# Use sql_head to check cases
## sql_head(table_name='violation_descriptions')

## Get column names and datatypes from newly created table
conn, cur = get_conn_cur()
cur = conn.cursor()
uq = """SELECT column_name, data_type
          FROM information_schema.columns
          WHERE table_name = 'violation_descriptions';"""
cur.execute(uq)
## print(cur.fetchall())
conn.close()

## For loop to get everything in violations_df
data_tups = [tuple(x) for x in violation_desc_df.to_numpy()]

## Check values
##data_tups[2]

## Check query
iq = """INSERT INTO violation_descriptions(violation_section,violation_type,charge_description,violation_id) VALUES(%s, %s, %s, %s);"""

## Check query
##iq % data_tups[2]

'''
## Upload to table in database
conn, cur = get_conn_cur()
cur.executemany(iq, data_tups)
conn.commit()
conn.close()
'''
"""## Check
 
Perform some SQL check to validate that your data is in the database.  Do a basic select and filter, or a simple join, for example. 
"""

## Test to see if data was uploaded correctly
sq = """ SELECT * FROM violations
          LIMIT 5;"""
print(run_query(sq))
print('\n')
print('\n')

"""### It matches violations_df above"""

## Test to see if data was uploaded correctly
sq = """ SELECT * FROM violation_descriptions
          LIMIT 5;"""
print(run_query(sq))

"""### It matches violation_desc_df from above"""