from sklearn.model_selection import GridSearchCV
import pickle
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import sys
import yaml
import os
import numpy as np
from sklearn.metrics import accuracy_score



def read_yaml(file_path):
    try:
        logging.info("Enter the read_yaml method")
        with open(file_path,"r") as file:
            return yaml.safe_load(file)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def write_yaml(file_path,content,replace=False):
    try:
        logging.info("Enter the write_yaml method")
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array(file_path: str, array: np.ndarray) -> None:
    try:
        logging.info("Enter the save_numpy_array method")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_object(file_path: str, object: object) -> None:
    try:
        logging.info("Enter the save_object method")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(object, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def evaluate_model(x_train,x_test,y_train,y_test,models,params):
    try:
        logging.info("Enter the evaluate_model method")
        model_list={}
        model_score={}
        for model_name, model in models.items():
            param=params[model_name]
            gridsearch=GridSearchCV(estimator=model,param_grid=param,cv=3,n_jobs=-1)

            gridsearch.fit(x_train,y_train)

            model.set_params(**gridsearch.best_params_)
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)
            accuracy_train=accuracy_score(y_train,y_train_pred)
            accuracy_test=accuracy_score(y_test,y_test_pred)
            model_list[model_name]=model
            model_score[model_name]=accuracy_test
        
        return model_list,model_score
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise ValueError("File not found")
        logging.info("Enter the load_object method")
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_numpy_array(file_path: str) -> np.ndarray:
    try:
        if not os.path.exists(file_path):
            raise ValueError("File not found")
        logging.info("Enter the load_numpy_array method")
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
