from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact
from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.entity.artifact_entity import DataValidationArtifact
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.constant.training_pipeline import TARGET_COLUMN_NAME,DATA_TRANSFORMATION_IMPUTE_PARAMS
from NetworkSecurity.utils.main_utils.utils import save_object,save_numpy_array
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import os
import sys
import numpy as np
import pandas as pd

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        self.data_transformation_config=data_transformation_config
        self.data_validation_artifact=data_validation_artifact
        
    @staticmethod
    def read_data(file_path):
        try:
            logging.info("Enter the read_data method of DataTransformation class")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_transformation_object(cls):
        try:
            logging.info("Enter the get_transformation_object method of DataTransformation class")
            
            knn_imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)#this knn imputer takes the n_neighbors and weights as parameters and imputes the missing values by calculating the mean of the nearest neighbors
            processor=Pipeline(steps=[
                ("imputer",knn_imputer)
            ])
            return processor
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Enter the initiate_data_transformation method of DataTransformation class")
            train_df=self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=self.read_data(self.data_validation_artifact.valid_test_file_path)

            input_train_features=train_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_train_features=train_df[TARGET_COLUMN_NAME]
            input_test_features=test_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_test_features=test_df[TARGET_COLUMN_NAME]

            preprocessor=self.get_transformation_object()

            processor_obj=preprocessor.fit(input_train_features)
            transformed_train_features=processor_obj.transform(input_train_features)
            transformed_test_features=processor_obj.transform(input_test_features)


            train_array=np.c_[transformed_train_features,target_train_features]
            test_array=np.c_[transformed_test_features,target_test_features]


            save_numpy_array(file_path=self.data_transformation_config.data_transformation_transformed_train_file_path,array=train_array)
            save_numpy_array(file_path=self.data_transformation_config.data_transformation_transformed_test_file_path,array=test_array)
            save_object(file_path=self.data_transformation_config.data_transformation_transformed_object_file_path,object=processor_obj)



            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformation_transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformation_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformation_transformed_test_file_path
            )
            logging.info("Data transformation artifact created")
            return data_transformation_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)