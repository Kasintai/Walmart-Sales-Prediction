# Walmart Weekly Sales Prediction - End-to-End ML Project
<br/>

<p align="center">
  <img width="666" alt="Image" src="https://github.com/user-attachments/assets/9dd81b8c-da73-445a-8abd-3447a8f47eb3" />
</p>
<p align="center">
  <a href="http://load-balancer1-1863200110.ap-southeast-2.elb.amazonaws.com/predictdata">
    http://load-balancer1-1863200110.ap-southeast-2.elb.amazonaws.com/predictdata
  </a>
</p>

## Project Overview:
This project is an end-to-end machine learning system designed to predict weekly sales for Walmart stores based on historical data. It integrates machine learning, web development, database management, and cloud deployment to provide users with real-time sales predictions.
<br/>

## Key Components
### 1. Machine Learning Model

- **Goal:** Predict weekly sales for each Walmart store.
- **Dataset:** Kaggle's Walmart dataset (train.csv, test.csv, stores.csv, features.csv).
  - https://www.kaggle.com/competitions/walmart-recruiting-store-sales-forecasting

- **Feature Engineering:**
  - Merged train/test datasets with stores and features datasets for richer insights.
  - Extracted Year, Month, Day, and Day of the Week from dates.
  - Cyclical encode: Applying sin/cos transformations to capture seasonality.

- **Model:** CatBoost Regressor

- **Performance Metrics:**
  - R² Score: 0.86
<br/>

### 2. Web Application (Flask + HTML/CSS/JS)

- **Frontend:**
  - HTML & CSS for structure and styling.
  - JavaScript for form validation & AJAX requests.
  - Uses Flask's Jinja2 templating for dynamic content updates.

- **Backend:**
  - Flask API to handle user inputs and serve predictions.
  - Stores user inputs and predictions in PostgreSQL.
<br/>

### 3. Database (PostgreSQL)

- Stores user input and predictions persistently.
- Schema: Stores predictions with fields (store number, department, date, holiday status, predicted sales, timestamp).
- Manual Clearing: Users can reset the database via a "Refresh Database" button.
- No data retention policy yet, meaning all predictions accumulate over time.
<br/>

### 4. Cloud Deployment (AWS ECS + Fargate)

- **Pipeline:**
  - Code push triggers GitHub Actions.
  - Builds and pushes a Docker image to AWS ECR.
  - Deploys the latest image to AWS ECS (Fargate).

- **Current Scaling Setup:**
  - Runs one ECS task, meaning no autoscaling is enabled.
  - Future improvements may involve adding load balancing or Redis caching.
<br/>

### 5. CI/CD Pipeline (GitHub Actions)

- **Continuous Integration (CI):**
  - Triggers on push to main branch.
  - Builds and pushes Docker image to AWS ECR.

- **Continuous Deployment (CD):**
  - Updates ECS Service to deploy the latest Docker image.
  - Missing CI Enhancements:
 <br/>

