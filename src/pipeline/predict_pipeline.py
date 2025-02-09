import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            # preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            print("After Loading")
            # preprocessor=load_object(file_path=preprocessor_path)
            # print("After Loading")
            # data_scaled=preprocessor.transform(features)
            # preds=model.predict(data_scaled)

            obj_ingestion = DataIngestion()
            merge_df = obj_ingestion.merge_dataframes(features)

            obj_transformation = DataTransformation()
            merge_df = obj_transformation.feature_engineer(merge_df)
            merge_df = obj_transformation.convert_column_type(merge_df)
            # print(merge_df)
            # print(merge_df.info())

            preds = model.predict(merge_df)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self, store: int, dept: int, date, is_holiday: bool): #weekly_sales, datetime
        self.store = store
        self.dept = dept
        self.date = date
        # self.weekly_sales = weekly_sales
        self.is_holiday = is_holiday

    def get_data_as_data_frame(self):
        """
        Convert input data into a pandas DataFrame.
        """
        try:
            data_dict = {
                "Store": [self.store],
                "Dept": [self.dept],
                "Date": [self.date],
                # "Weekly_Sales": [self.weekly_sales],
                "IsHoliday": [self.is_holiday]
            }
            return pd.DataFrame(data_dict)
        except Exception as e:
            raise CustomException(e, sys)


