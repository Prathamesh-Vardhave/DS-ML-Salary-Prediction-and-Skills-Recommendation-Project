# DS-ML Salary Prediction and Skills Recommendation Project

End-to-end Machine Learning project for salary prediction and skill recommendations using FastAPI (backend) and Streamlit (frontend).

## Overview

This project predicts salary based on job role, experience, city, and skills. It also recommends relevant skills based on job patterns learned from data.

The system includes:
- Feature engineering pipeline
- XGBoost trained model
- FastAPI backend for serving predictions
- Streamlit frontend for interactive UI

## Project Structure

DS-ML-Salary-Prediction-and-Skills-Recommendation-Project/

- backend/ → FastAPI application  
- frontend/ → Streamlit UI  
- Model/ → Trained ML models (.pkl files)  
- notebooks → Model experimentation  
- README.md  

## Dataset

The dataset used in this project is publicly available on Kaggle:

Kaggle Dataset Link:  
https://www.kaggle.com/datasets/prathameshvardhave07/data-science-jobs-salary-prediction

The full dataset is not included in this repository due to size limitations.  
Please download it manually and place it in the project directory before running notebooks.

## Model Details

- Algorithm: XGBoost Regressor  
- Model saved using joblib (.pkl format)  
- Includes mapping files for job role and city encoding  

## Author

Prathamesh Vardhave  
Computer Engineering | Machine Learning  

