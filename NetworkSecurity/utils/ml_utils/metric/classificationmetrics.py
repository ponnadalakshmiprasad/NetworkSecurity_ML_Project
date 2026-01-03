from NetworkSecurity.entity.artifact_entity import ModelTrainerMetricArtifact
from sklearn.metrics._classification import classification_report
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import sys
from sklearn.metrics import f1_score,precision_score,recall_score



def classification_metrics(y_true,y_pred)->ModelTrainerMetricArtifact:
    try:
        f1=f1_score(y_true,y_pred)
        precision=precision_score(y_true,y_pred)
        recall=recall_score(y_true,y_pred)
        classification_report=ModelTrainerMetricArtifact(f1_score=f1,precision=precision,recall=recall)
        return classification_report
    except Exception as e:
        raise NetworkSecurityException(e,sys)