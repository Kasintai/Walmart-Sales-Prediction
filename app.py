from flask import Flask, request, render_template
import pandas as pd
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    '''
    Note: Input predictor values [Store, Department, Date, Is_Holday] must exist in df_test_2 (i.e. select input values form df_test_2)
    (Refer to df_test_2 from Walmart_1 (04/02/2025).ipynb in google colab)

    index.html --> http://127.0.0.1:5000
    home.html --> http://127.0.0.1:5000/predictdata

    127.0.0.1 --> is localhost (your own computer).
    5000 --> is the default port Flask uses.
    '''

    if request.method == 'GET':
        return render_template('home.html')
    else: #request.method == 'POST':

        # Get / retrieve user input from form and create input data object
        data = CustomData(
            store=int(request.form.get('store')),
            dept=int(request.form.get('dept')),
            date=request.form.get('date'),
            # weekly_sales=float(request.form.get('weekly_sales')),
            # is_holiday=int(request.form.get('is_holiday'))
            is_holiday = request.form.get('is_holiday') == "True"
        )

        # Convert user input to DataFrame
        pred_df = data.get_data_as_data_frame()

        # Predict using the predict pipeline
        obj_predict_pipeline=PredictPipeline()
        results = obj_predict_pipeline.predict(pred_df)

        # # Step 1: Merge with store and feature data
        # ingestion = DataIngestion()
        # merged_df = ingestion.ingest_input_data(input_df)

        # # Step 2: Apply transformation
        # transformer = DataTransformation()
        # transformed_df = transformer.transform_input_data(merged_df)

        # # Step 3: Predict Weekly_Sales
        # model_trainer = ModelTrainer()
        # prediction = model_trainer.predict_input_data(transformed_df)

        return render_template('home.html', results=results[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
