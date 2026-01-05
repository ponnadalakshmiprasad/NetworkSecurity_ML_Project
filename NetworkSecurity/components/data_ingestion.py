from NetworkSecurity.utils.main_utils.utils import save_object
from bokeh.layouts import column
from dotenv import load_dotenv
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import pymongo
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split
load_dotenv()
mongodb_url=os.getenv("MONGODB_URL")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config

    def collection_of_data(self):
        try:
            logging.info("Enter the collection_data method")
            collection_name=self.data_ingestion_config.collection_name
            database_name=self.data_ingestion_config.database_name
            self.mongo_client=pymongo.MongoClient(mongodb_url)
            self.data=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(self.data.find()))

            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)

            if "index" in df.columns:
                df=df.drop(columns=["index"])

            return df
            

        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def data_ingestion_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info("Enter the data_ingestion_feature_store method")
            feature_store_path=self.data_ingestion_config.data_ingestion_feature_store_path
            print(feature_store_path)
            #creating directory
            dir_path=os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("The feature store directory is created")
            print(dir_path)
            print(feature_store_path)
            dataframe.to_csv(feature_store_path,index=False,header=True)
            return dataframe
            


        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def data_train_test_split(self,dataframe1:pd.DataFrame):
        try:
            logging.info("Enter the data_train_test_split method")
            features_names=list(dataframe1.columns)
            print(features_names)

            os.makedirs(os.path.dirname(self.data_ingestion_config.features_name_file_path),exist_ok=True)

            save_object(file_path=self.data_ingestion_config.features_name_file_path,object=features_names)

            save_object("final_model/features_names.pkl",features_names)

            train_set,test_set=train_test_split(dataframe1,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)

            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path),exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("Enter the initiate_data_ingestion method")
            dataframe=self.collection_of_data()
            dataframe1=self.data_ingestion_feature_store(dataframe)
            self.data_train_test_split(dataframe1)
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,tested_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)