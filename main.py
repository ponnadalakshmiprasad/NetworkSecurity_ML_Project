from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from NetworkSecurity.components.data_transformation import DataTransformation
import sys
from NetworkSecurity.entity.config_entity import ModelTrainerConfig
from NetworkSecurity.components.model_trainer import ModelTrainer




if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataconfig)
        logging.info("Data Ingestion started")
        dataconfigurationartifact=dataingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(dataconfigurationartifact)
        

        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        datavalidation=DataValidation(dataconfigurationartifact,datavalidationconfig)
        logging.info("Data Validation started")
        datavalidationartifact=datavalidation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(datavalidationartifact)


        datatransformationconfig=DataTransformationConfig(trainingpipelineconfig)
        datatransformation=DataTransformation(datatransformationconfig,datavalidationartifact)
        logging.info("Data Transformation started")
        datatransformationartifact=datatransformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        print(datatransformationartifact)

        modeltrainerconfig=ModelTrainerConfig(trainingpipelineconfig)
        modeltrainer=ModelTrainer(modeltrainerconfig,datatransformationartifact)
        logging.info("Model Training started")
        modeltrainerartifact=modeltrainer.initiate_model_trainer()
        logging.info("Model Training completed")
        print(modeltrainerartifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)