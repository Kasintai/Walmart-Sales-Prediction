from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

# Function‐oriented approach
# def start_training_pipeline():
#     """
#     Orchestrate the data ingestion, transformation, and model training steps.
#     """
#     # 1. Data Ingestion
#     ingestion = DataIngestion()
#     train_data_path, test_data_path = ingestion.initiate_data_ingestion()

#     # 2. Data Transformation
#     transformer = DataTransformation()
#     train_df, test_df = transformer.initiate_data_transformation(train_data_path, test_data_path)

#     # 3. Model Training
#     trainer = ModelTrainer()
#     r2_score, mae_score = trainer.initiate_model_trainer(train_df, test_df)

#     # Print out or log the final metrics
#     print("Training complete.")
#     print(f"Best Model R2 Score  : {r2_score}")
#     print(f"Best Model MAE Score : {mae_score}")

# if __name__ == "__main__":
#     start_training_pipeline()

# or:

# Class‐based approach
# If we prefer a more object‐oriented design (perhaps to store configuration in an object, reuse pipeline state, etc.),
# we could create a TrainPipeline class. It may look like:
class TrainPipeline:
    def __init__(self):
        self.ingestor = DataIngestion()
        self.transformer = DataTransformation()
        self.trainer = ModelTrainer()

    def run(self):
        train_data_path, test_data_path = self.ingestor.initiate_data_ingestion()
        train_df, test_df = self.transformer.initiate_data_transformation(train_data_path, test_data_path)
        r2, mae = self.trainer.initiate_model_trainer(train_df, test_df)
        print(r2, mae)

if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run()

# Need to test by running in the terminal prompt: python src/pipeline/train_pipeline.py
# (venv) (base) kasinm@Kasins-MacBook-Pro-2 Walmart_2 % python src/pipeline/train_pipeline.py

