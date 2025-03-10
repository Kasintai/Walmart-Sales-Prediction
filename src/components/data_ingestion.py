import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass #

from src.components.data_transformation import DataTransformation

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train_.csv')
    test_data_path: str = os.path.join('artifacts', 'test_.csv')
    raw_data_path: str=os.path.join('artifacts', 'full_data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def merge_dataframes(self, df_train):
        """Merge train data with store and feature datasets."""
        try:
            logging.info("Merging train data with store and feature datasets.")
            df_store = pd.read_csv('notebook/data/stores.csv')
            df_feature = pd.read_csv('notebook/data/features.csv')

            # Merge train data with store details
            df_merge = pd.merge(df_train, df_store, on='Store', how='inner')

            # Convert Date columns to datetime format
            df_merge['Date'] = pd.to_datetime(df_merge['Date'])
            df_feature['Date'] = pd.to_datetime(df_feature['Date'])

            # Drop 'IsHoliday' column from features to avoid redundancy
            df_feature.drop(columns=['IsHoliday'], axis=1, inplace=True)

            # Merge with feature dataset on 'Store' and 'Date'
            df_merge = pd.merge(df_merge, df_feature, on=['Store', 'Date']) #, how='left'
            # df_merge['Date'] = pd.to_datetime(df_merge['Date']) #
            logging.info("Dataframes merged successfully.")

            return df_merge

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Convert csv to df
            df_train = pd.read_csv('notebook/data/train.csv')
            # df_test = pd.read_csv('notebook/data/test.csv')

            # df_store = pd.read_csv('notebook/data/stores.csv')
            # df_feature = pd.read_csv('notebook/data/features.csv')
            logging.info("Read the dataset as dataframe")

            # # Construct the full dataset
            # df_merge = pd.merge(df_train, df_store, on='Store') #inner join

            # df_merge['Date'] = pd.to_datetime(df_merge['Date'])
            # df_feature['Date'] = pd.to_datetime(df_feature['Date'])

            # df_feature.drop(columns=['IsHoliday'], axis=1, inplace=True)
            # df_merge = pd.merge(df_merge, df_feature, on=['Store', 'Date'])
            # # df_merge['Date'] = pd.to_datetime(df_merge['Date']) #
            # logging.info("Merge dataframe to form full dataset")

            # Merge datasets
            df_merge = self.merge_dataframes(df_train)

            # os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            # df_merge.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            # Ensure both directories exist before saving
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok=True)
            df_merge.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df_merge, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)

# if __name__=="__main__":
#     obj=DataIngestion()
#     train_data,test_data=obj.initiate_data_ingestion()

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    # Apply transformation
    data_transformation = DataTransformation()
    train_data, test_data = data_transformation.initiate_data_transformation(train_data, test_data)
    print(train_data.info())

    # # # Train model
    # modeltrainer = ModelTrainer()
    # r2_score, mae_score = modeltrainer.initiate_model_trainer(train_data, test_data)
    # print(f"r2 score: {r2_score}")
    # print(f"MAE score: {mae_score}")

