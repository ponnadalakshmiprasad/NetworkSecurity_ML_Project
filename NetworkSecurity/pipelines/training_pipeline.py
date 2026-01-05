import sys
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.model_trainer import ModelTrainer
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from NetworkSecurity.logging.logger import logging






class TrainingPipeline:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.training_pipeline_config=training_pipeline_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            data_transformation=DataTransformation(data_transformation_config=self.data_transformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def run_pipeline(self):
        try:
            logging.info("Starting Data Ingestion")
            data_ingestion_artifact=self.data_ingestion()
            logging.info("Data Ingestion completed")

            logging.info("Starting Data Validation")
            data_validation_artifact=self.data_validation(data_ingestion_artifact=data_ingestion_artifact)
            logging.info("Data Validation completed")

            logging.info("Starting Data Transformation")
            data_transformation_artifact=self.data_transformation(data_validation_artifact=data_validation_artifact)
            logging.info("Data Transformation completed")

            logging.info("Starting Model Trainer")
            model_trainer_artifact=self.model_trainer(data_transformation_artifact=data_transformation_artifact)
            logging.info("Model Trainer completed")

            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_training_pipeline(self):
        try:
            logging.info("Enter the initiate_training_pipeline method of TrainingPipeline class")
            self.model_trainer_artifact=self.run_pipeline()
            logging.info("Training Pipeline completed")
            return self.model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)