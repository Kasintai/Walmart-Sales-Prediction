import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

class DataTransformation:
    def __init__(self):
        pass  # No need to define file paths since we won't save files.


    def feature_engineer(self, df):
        try:
            logging.info("Applying feature engineering")
            df["Date"] = pd.to_datetime(df["Date"]) #, errors='coerce'
            
            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month
            df["Day"] = df["Date"].dt.day

            df["Month_Sin"] = np.sin(2 * np.pi * df["Month"] / 12)
            df["Month_Cos"] = np.cos(2 * np.pi * df["Month"] / 12)
            df["DayOfWeek"] = df["Date"].dt.dayofweek

            df.drop(columns=["Date"], axis=1, inplace=True)

            return df
        except Exception as e:
            raise CustomException(e, sys)
    

    def convert_column_type(self, df):
        try:
            logging.info("Converting bool and obj type to int and str")

            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].astype(str)
                elif df[col].dtype == "bool":
                    df[col] = df[col].astype(int)
            
            return df
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path) #, parse_dates=["Date"])
            test_df = pd.read_csv(test_path) #, parse_dates=["Date"])
            logging.info("Read train and test data successfully")

            # Convert data types
            train_df = self.convert_column_type(train_df)
            test_df = self.convert_column_type(test_df)

            train_df = self.feature_engineer(train_df)
            test_df = self.feature_engineer(test_df)

            logging.info("Data transformation completed")

            return train_df, test_df  # Returns DataFrames instead of saving CSV files.

        except Exception as e:
            raise CustomException(e, sys)
