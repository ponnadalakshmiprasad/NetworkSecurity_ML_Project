from distributed.core import error_message
from scipy.stats._mstats_basic import ks_2samp
from NetworkSecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import sys
import os
from NetworkSecurity.utils.main_utils.utils import read_yaml,write_yaml
import scipy
from NetworkSecurity.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
import pandas as pd


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        try:
            logging.info("Enter the validate_number_of_columns method")
            number_of_columns=len(self.schema_config["columns"])
            if len(dataframe.columns)!=number_of_columns:
                return False
            logging.info("Number of columns is matching")
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def drift_dataset_report(self,train_data,test_data,threshold=0.05):
        try:
            logging.info("Enter the drift_dataset_report method")
            status=True
            report={}
            for column in train_data.columns:
                d1=train_data[column]
                d2=test_data[column]
                is_same_distribution=ks_2samp(d1,d2)
                if is_same_distribution.pvalue<=threshold:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{"p_value":is_same_distribution.pvalue,"is_found":is_found}})
            drift_report_file_path=self.data_validation_config.data_valid_drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml(file_path=drift_report_file_path,content=report,replace=True)

            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_data_validation(self):
        try:
            logging.info("Enter the data_validation method")
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.tested_file_path

            #read the data
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)


            #validate the data
            status=self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message=f"Number of columns is not matching"
            status=self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message=f"Number of columns is not matching"

            #drift_report of the data
            status=self.drift_dataset_report(train_dataframe,test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.data_valid_drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            #save the valid data
            os.makedirs(os.path.dirname(self.data_validation_config.training_valid_data_file_path),exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.training_valid_data_file_path,index=False,header=True)
            os.makedirs(os.path.dirname(self.data_validation_config.testing_valid_data_path),exist_ok=True)
            test_dataframe.to_csv(self.data_validation_config.testing_valid_data_path,index=False,header=True)
            


            datavalidationartifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.training_valid_data_file_path,
                valid_test_file_path=self.data_validation_config.testing_valid_data_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.data_valid_drift_report_file_path
            )


            return datavalidationartifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

