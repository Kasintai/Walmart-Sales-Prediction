from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

from src.database import save_prediction, get_predictions  # Import database functions

application = Flask(__name__)
app = application

#####
from src.database import refresh_table

@app.route("/refresh", methods=["POST"])
def refresh():
    refresh_table()
    return "Database table refreshed!", 200
#####

@app.route('/')
def index():
    return render_template('index.html')

#####
import logging
logging.basicConfig(level=logging.DEBUG)

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

    logging.debug(f"🔥 New Request: {request.method} - Headers: {request.headers}")  # ✅ Log request method

    if request.method == 'GET':
        # Fetch past predictions to display on the page
        predictions = get_predictions()
        logging.debug("✅ Returning GET request to display previous predictions.")  # ✅ Log GET return
        return render_template('home.html', predictions=predictions)
    
        # return render_template('home.html')
        
    else: #request.method == 'POST':
        logging.debug("🛠 Handling POST request - Processing Prediction")  # ✅ Log POST start


        # # Get / retrieve user input from form and create input data object
        # data = CustomData(
        #     store=int(request.form.get('store')),
        #     dept=int(request.form.get('dept')),
        #     date=request.form.get('date'),
        #     # weekly_sales=float(request.form.get('weekly_sales')),
        #     # is_holiday=int(request.form.get('is_holiday'))
        #     is_holiday = request.form.get('is_holiday') == "True"
        # )

        # # Convert user input to DataFrame
        # pred_df = data.get_data_as_data_frame()

        # # Predict using the predict pipeline
        # obj_predict_pipeline=PredictPipeline()
        # results = obj_predict_pipeline.predict(pred_df)

        # # # Step 1: Merge with store and feature data
        # # ingestion = DataIngestion()
        # # merged_df = ingestion.ingest_input_data(input_df)

        # # # Step 2: Apply transformation
        # # transformer = DataTransformation()
        # # transformed_df = transformer.transform_input_data(merged_df)

        # # # Step 3: Predict Weekly_Sales
        # # model_trainer = ModelTrainer()
        # # prediction = model_trainer.predict_input_data(transformed_df)

        # # Save prediction to database
        # save_prediction(store_number, department_number, date, is_holiday, predicted_sales)

        # # Fetch updated predictions
        # predictions = get_predictions()

        # return render_template('home.html', results=round(results[0], 2))

        ##########

        # Get user input
        store_number = int(request.form.get('store'))
        department_number = int(request.form.get('dept'))
        date = request.form.get('date')
        is_holiday = request.form.get('is_holiday') == "True"

        # Convert input into a DataFrame
        data = CustomData(
            store=store_number,
            dept=department_number,
            date=date,
            is_holiday=is_holiday
        )
        pred_df = data.get_data_as_data_frame()

        # Predict sales
        obj_predict_pipeline = PredictPipeline()
        results = obj_predict_pipeline.predict(pred_df)
        predicted_sales = round(results[0], 2)

        logging.debug(f"🔢 Prediction Complete: Store={store_number}, Dept={department_number}, Date={date}, Holiday={is_holiday}, Sales={predicted_sales}")

        # Save prediction to database
        # save_prediction(store_number, department_number, date, is_holiday, predicted_sales)

        # Fetch updated predictions
        predictions = get_predictions()

        logging.debug("💾 Prediction saved to database.")  # ✅ Log after saving

        return render_template('home.html', results=predicted_sales, predictions=predictions)
        # return redirect(url_for('predict_datapoint'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
