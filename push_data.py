# For large or continuously arriving data from external systems such as S3 or client servers, we ingest the data into a database first. 
# This allows scalable storage, incremental updates, and reproducible ML pipelines before creating training and test datasets.


# For a static dataset, direct ingestion is sufficient.
# However, in production ML systems, data is often stored in databases to support incremental updates, multiple data sources, and reproducibility.
# MongoDB acts as a centralized raw data store before feature engineering and train-test splitting.
import certifi
import os
import sys
import json
import pymongo
import pandas as pd
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()
mongodb_url=os.getenv("MONGO_DB_URL")

ca=certifi.where()#certifi.where() returns the file path to the trusted CA certificate bundle used for SSL verification.
#certifi.where() returns the file path to the trusted CA certificate bundle used for SSL verification.




class NetworkSecurityDataPusher:#for extracting the data form the csv file and pushing it to the mongodb
    def __init__(self):
        pass
    def csv_to_json_conversion(self,file_path):
        try:
            logging.info("Enter the csv_to_json_conversion method")
            data=pd.read_csv(file_path)#reading the csv file using the as argument
            data.reset_index(drop=True, inplace=True)#Reset the DataFrame index to a clean sequential index (0,1,2,…), discard the old index, and apply the change directly to data.”
            records=json.loads(data.to_json(orient="records"))
            # records=list(json.loads(data.T.to_json()).values())
            # data.T is used to transpose the DataFrame
            # (rows become columns and columns become rows)

            # This transposed DataFrame is then converted to JSON using to_json().
            # By default, to_json() uses orient="columns", so it produces a
            # dictionary of dictionaries in the form:
            # {
            #   "index": {"column1": value1, "column2": value2, ...},
            #   "index": {"column1": value1, "column2": value2, ...},
            #   "index": {"column1": value1, "column2": value2, ...},
            #   ...
            # }
            # Here:
            #   - outer keys ("index") are the original DataFrame row indices
            #   - inner keys ("column1", "column2", ...) are the original column names


            # Without doing transpose and using the default orient="columns",
            # data.to_json() converts the DataFrame into the following structure:
            #
            # {
            #   "column1": {"index1": value1, "index2": value2, ...},
            #   "column2": {"index1": value1, "index2": value2, ...},
            #   "column3": {"index1": value1, "index2": value2, ...},
            #   ...
            # }
            #
            # Here:
            # - The outer keys ("column1", "column2", ...) are the DataFrame column names
            # - The inner keys ("index1", "index2", ...) are the row indices
            # - The inner values are the corresponding cell values



            # data.T.to_json() returns a JSON STRING, not a Python object,
            # so json.loads() is used to convert that JSON string into a Python dictionary

            # We then call .values() on the dictionary to discard the index keys
            # and keep only the row-wise dictionaries

            # list() is used to convert the dict_values object into a list,
            # resulting in a list of row dictionaries like:
            # [
            #   {"column1": value1, "column2": value2, ...},
            #   ...
            # ]

            # NOTE:
            # The same result can be achieved more directly using:
            # records = json.loads(data.to_json(orient="records"))
            #
            # Here, orient="records" directly converts the DataFrame into a
            # list of row-wise dictionaries, without needing transpose.
            #
            # orient="records" prioritizes rows, producing output like:
            # [
            #   {"column1": value1, "column2": value2, ...},
            #   {"column1": value1, "column2": value2, ...},
            #   {"column1": value1, "column2": value2, ...},
            #   ...
            # ]


            #hint:
            #orient="columns"  →  { column : { index : value } }
            #orient="records"  →  [ { column : value }, ... ]
            #transpose + columns → { index : { column : value } }
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def push_data_to_mongodb(self,records,database,collections):
        try:
            self.database=database
            self.collections=collections
            self.records=records
            logging.info("Enter the push_data_to_mongodb method")
            self.mongo_client=pymongo.MongoClient(mongodb_url)
            #Creates a connection object to a MongoDB server
            #mongodb_url contains:
            #host
            #port
            #username/password (optional)
            #database options (SSL, auth, etc.)

            #This does not insert data
            #It only establishes a connection


            #self.mongo_client is the connection object

            self.database=self.mongo_client[self.database]
            #self.mongo_client behaves like a dictionary
            #self.database (string) is the database name
            #self.database is the database object
            
            self.collections=self.database[self.collections]
            #self.collections is a collection name (string)
            #A collection is similar to a table in SQL
            #self.collection is the collection object



            self.collections.insert_many(self.records)
            #Inserts multiple documents at once into MongoDB
            #self.records must be:
            #a list of dictionaries




            #overall flow of push_data_to_mongodb method:
            # MongoClient created
            #         ↓
            # Database selected
            #         ↓
            # Collection selected
            #         ↓
            # Multiple documents inserted


            logging.info("Data pushed to mongodb")
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    try:
        logging.info("Enter the main method")
        push_data=NetworkSecurityDataPusher()
        database="NetworkSecurity"
        collections="NetworkSecurity_data"
        File_Path="/Users/prasad/Desktop/ML_practice/ML_Resume_Projects/NetworkSecurity_ML_project/network_data/phisingData.csv"
        records=push_data.csv_to_json_conversion(file_path=File_Path)
        # print(records)
        no_of_records=push_data.push_data_to_mongodb(records,database,collections)
        logging.info(f"no of records pushed to mongodb:{no_of_records}")
        print(no_of_records)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



#phase1:
# .env
#   ↓
# mongodb_url (secure)


#phase2:
# csv_to_json_conversion
#   ↓
# CSV → DataFrame → list[dict]



#phase3:
# push_data_to_mongodb
#   ↓
# MongoClient (TLS)
#   ↓
# Database
#   ↓
# Collection
#   ↓
# insert_many(records)




#phase4:
# logger.py
#   ↓
# Single logging config used everywhere



#phase5:
# exception.py
#   ↓
# Consistent error reporting with traceback




