# Walmart Weekly Sales Prediction - End-to-End ML Project

## Project Overview:
This project is an end-to-end machine learning system designed to predict weekly sales for Walmart stores based on historical data. It integrates machine learning, web development, database management, and cloud deployment to provide users with real-time sales predictions.

## Key Components
1. Machine Learning Model (CatBoost Regressor)

Goal: Predict weekly sales for each Walmart store.
Dataset Used: Kaggle's Walmart dataset (train.csv, test.csv, stores.csv, features.csv).
Feature Engineering:
Extracted Year, Month, Day, and Day of the Week from dates.
Applied sin/cos transformations for seasonality.
Merged store and feature datasets for richer insights.
Performance Metrics:
R² Score: 0.86
RMSE: 8,454


2. Web Application (Flask + HTML/CSS/JS)

Frontend:
HTML & CSS for structure and styling.
JavaScript for form validation & AJAX requests.
Uses Flask's Jinja2 templating for dynamic content updates.
Backend:
Flask API to handle user inputs and serve predictions.
Stores user inputs and predictions in PostgreSQL.


3. Database (PostgreSQL)

Stores user input and predictions persistently.
Schema: Stores predictions with fields (store number, department, date, holiday status, predicted sales, timestamp).
Manual Clearing: Users can reset the database via a "Refresh Database" button.
No data retention policy yet, meaning all predictions accumulate over time.


4. Cloud Deployment (AWS ECS + Fargate)

Pipeline:
Code push triggers GitHub Actions.
Builds and pushes a Docker image to AWS ECR.
Deploys the latest image to AWS ECS (Fargate).
Current Scaling Setup:
Runs one ECS task, meaning no autoscaling is enabled.
Future improvements may involve adding load balancing or Redis caching.


5. CI/CD Pipeline (GitHub Actions)

✅ Continuous Integration (CI):
Triggers on push to main branch.
Builds and pushes Docker image to AWS ECR.
✅ Continuous Deployment (CD):

Updates ECS Service to deploy the latest Docker image.
🚧 Missing CI Enhancements:
❌ Automated Testing (Unit/API tests)
❌ Linting & Code Quality Checks (black, pylint, flake8)
❌ Security Scanning (Docker vulnerabilities)

