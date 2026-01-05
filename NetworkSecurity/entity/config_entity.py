import os
import sys
from NetworkSecurity.constant import training_pipeline
from datetime import datetime
 
class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%Y-%m-%d-%H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp: str=timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)

        self.data_ingestion_feature_store_path=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        self.data_ingestion_ingested_dir=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR)

        self.training_file_path=os.path.join(self.data_ingestion_ingested_dir,training_pipeline.TRAIN_FILE_NAME)

        self.testing_file_path=os.path.join(self.data_ingestion_ingested_dir,training_pipeline.TEST_FILE_NAME)

        self.features_name_dir=os.path.join(self.data_ingestion_ingested_dir,training_pipeline.DATA_INGESTION_FEATURE_NAME_DIR)

        self.features_name_file_path=os.path.join(self.features_name_dir,training_pipeline.DATA_INGESTION_FEATURES_NAME_FILE)
        
        self.train_test_split_ratio=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
        
class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR)

        self.data_valid_data_path=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.data_invalid_data_dir=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)

        self.training_valid_data_file_path=os.path.join(self.data_valid_data_path,training_pipeline.TRAIN_FILE_NAME)

        self.testing_valid_data_path=os.path.join(self.data_valid_data_path,training_pipeline.TEST_FILE_NAME)

        self.training_invalid_data_file_path=os.path.join(self.data_invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)

        self.testing_invalid_data_path=os.path.join(self.data_invalid_data_dir,training_pipeline.TEST_FILE_NAME)

        self.data_valid_drift_report_file_path=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR)

        self.data_transformation_transformed_dir=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR)

        self.data_transformation_transformed_object_dir=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)

        self.data_transformation_transformed_train_file_path=os.path.join(self.data_transformation_transformed_dir,training_pipeline.TRAIN_FILE_NAME.replace(".csv",".npy"))

        self.data_transformation_transformed_test_file_path=os.path.join(self.data_transformation_transformed_dir,training_pipeline.TEST_FILE_NAME.replace(".csv",".npy"))
        
        self.data_transformation_transformed_object_file_path=os.path.join(self.data_transformation_transformed_object_dir,training_pipeline.PREPROCESSOR_OBJECT_FILE_NAME)


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR)
        self.model_trainer_transformed_object_file_path=os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.expected_score=training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfit_underfit_threshold=training_pipeline.MODEL_TRAINER_OVER_FIT_UNDER_FIT_THRESHOLD
        