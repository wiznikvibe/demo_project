import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

# @dataclass is a decorator used to xtend the functionality
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.datatransformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score','reading_score']
            categorical_columns =[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course',
            ]
            
            num_pipeline = Pipeline(
                steps = [
                    ("Imputer",SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler(with_mean=False))
                ])

            cat_pipeline = Pipeline(
                steps = [
                    ("Imputer",SimpleImputer(strategy='most_frequent')),
                    ("One_Hot_Encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("Numerical Columns scaling complete")
            logging.info("Categorical Columns encoding complete")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline",num_pipeline,numerical_columns),
                    ("categorical_pipeline",cat_pipeline,categorical_columns)

                ]
            )

            return preprocessor
                       
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading Data completed")
            logging.info("Obtaining preprocessing object")
            
            preprocessing_obj = self.get_data_transformer_object()
            target_column = "math_score"
            numerical_columns = ["writing_score","reading_score"]

            input_features_train = train_df.drop(columns=[target_column],axis=1)
            target_feature_train = train_df[target_column]

            input_features_test = test_df.drop(columns=[target_column],axis=1)
            target_feature_test = test_df[target_column]

            logging.info("Preprocessing Completed")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_features_train)
            input_feature_test_arr = preprocessing_obj.transform(input_features_test)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test)
            ]

            logging.info("Saved Preprocessing Object")

            save_object(file_path=self.datatransformation_config.preprocessor_obj_file_path, obj=preprocessing_obj)

            return (
                train_arr,
                test_arr,
                self.datatransformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)