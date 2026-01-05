from NetworkSecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os
import sys
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from sklearn.pipeline import Pipeline


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def predict(self,x):
        try:
            preprocessed_data=self.preprocessor.transform(x)
            return self.model.predict(preprocessed_data)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        