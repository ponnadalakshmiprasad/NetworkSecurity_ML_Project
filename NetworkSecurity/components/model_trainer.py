from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import sys
import os
from NetworkSecurity.utils.main_utils.utils import load_object,load_numpy_array,evaluate_model,save_object
from NetworkSecurity.utils.ml_utils.metric.classificationmetrics import classification_metrics
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.entity.artifact_entity import ModelTrainerArtifact
from NetworkSecurity.entity.config_entity import ModelTrainerConfig
from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier

import mlflow
import dagshub

#dagshub.init(repo_owner=,repo_name=,mlflow=)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def track_mlflow_metrics(self,model,test_classification_metric):
        try:
            logging.info("Enter the track_mlflow_metrics method")
            with mlflow.start_run():
                f1_score=test_classification_metric.f1_score
                precision=test_classification_metric.precision
                recall=test_classification_metric.recall

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision",precision)
                mlflow.log_metric("recall",recall)

                mlflow.sklearn.log_model(sk_model=model,name="model")
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            logging.info("Enter the train_model method")

            models={
                "RandomForestClassifier":RandomForestClassifier(),
                "GradientBoostingClassifier":GradientBoostingClassifier(),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "AdaBoostClassifier":AdaBoostClassifier()

            }

            params={
            "DecisionTreeClassifier": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "RandomForestClassifier":{
                #'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "GradientBoostingClassifier":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[0.1, 0.01],
                'n_estimators': [50, 100],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
            },
            "AdaBoostClassifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
            models,models_score=evaluate_model(x_train=x_train,x_test=x_test,y_train=y_train,y_test=y_test,models=models,params=params)
            best_model_name = max(models_score, key=models_score.get)

            best_model = models[best_model_name]
            best_score = models_score[best_model_name]

            y_train_pred=best_model.predict(x_train)
            y_test_pred=best_model.predict(x_test)

            train_classification_metric=classification_metrics(y_train,y_train_pred)
            test_classification_metric=classification_metrics(y_test,y_test_pred)


            #track mlflow metrics
            self.track_mlflow_metrics(best_model,train_classification_metric)
            self.track_mlflow_metrics(best_model,test_classification_metric)
            


            network_model=NetworkModel(preprocessor=self.data_transformation_artifact.transformed_object_file_path,model=best_model)

            save_object(file_path=self.model_trainer_config.model_trainer_transformed_object_file_path,object=network_model)

            save_object("final_model/model.pkl",best_model)
            save_object("final_model/preprocessor.pkl",self.data_transformation_artifact.transformed_object_file_path)

            model_trainer_artifact=ModelTrainerArtifact(trained_model_path=self.model_trainer_config.model_trainer_transformed_object_file_path,train_metric_artifact=train_classification_metric,test_metric_artifact=test_classification_metric)

            return model_trainer_artifact


            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("Enter the initiate_model_trainer method")
            train_array_path=self.data_transformation_artifact.transformed_train_file_path
            test_array_path=self.data_transformation_artifact.transformed_test_file_path


            train_array=load_numpy_array(train_array_path)
            test_array=load_numpy_array(test_array_path)

            x_train=train_array[:,:-1]
            y_train=train_array[:,-1]
            x_test=test_array[:,:-1]
            y_test=test_array[:,-1]


            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)

            return model_trainer_artifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)

