# Retail Sales Forecasting — Time Series Modeling Pipeline

**Masterschool | April 2026 Cohort**
**GitHub:** https://github.com/tomt-msit/timeseries-april

---

## Project overview

This project builds an end-to-end time series forecasting pipeline for retail demand prediction using daily sales data from Corporación Favorita, a large grocery retailer operating in the Guayas region of Ecuador.

The pipeline covers data cleaning, feature engineering, training five forecasting models, hyperparameter tuning, experiment tracking with MLflow, and a live interactive forecasting app built with Streamlit.

---

## Business problem

Retail demand forecasting is one of the most impactful applications of data science. Accurate forecasts help retailers:

- Reduce overstock and understock situations
- Plan staffing and logistics more effectively
- Improve supplier negotiations with better demand visibility
- Make pricing and promotion decisions based on predicted demand

---

## Dataset

| Section | Detail |
|---|---|

---

## Repository structure

```
timeseries-april/
│
├── data/                          # Data files (not committed — see Setup)
│   └── timeseries_with_features.csv
│
├── models/                        # Saved best model after training
│   ├── best_model.pkl
│   └── best_model_name.txt
│
├── mlruns/                        # MLflow experiment tracking folder
│
├── preparation/                   # Week 1 and 2 notebooks
│   ├── W1-Project_Prep.ipynb
│   ├── W1-Feature_Engineering.ipynb
│   ├── W2-ARIMA_Model.ipynb
│   ├── W2-ExpSmooth_Models.ipynb
│   ├── W2-Prophet_Model.ipynb
│   ├── W2-Statistical_Model.ipynb
│   ├── W3-XGBoost_Model.ipynb
│   └── W3-NN_Model.ipynb
│
├── W3-mlflow.ipynb                # Main pipeline: cleaning → models → MLflow
├── W3-streamlit.ipynb             # Streamlit tutorial and app building
│
├── app_prototype.py               # Streamlit forecasting app (final version)
├── hello_world.py                 # Streamlit Hello World demo
├── demo_layout.py                 # Streamlit layout components demo
├── demo_widgets.py                # Streamlit input widgets demo
├── demo_feedback.py               # Streamlit feedback components demo
│
├── requirements.txt               # All Python dependencies with versions
└── README.md                      # This file
```

---

## Methodology

### Data preparation (Week 1)

- Loaded and reviewed raw data
- Exploratory Data Analysis
- Feature Engineering

### Models trained (Weeks 2–3)

| Model | Type | Library |
|---|---|---|

### Evaluation metrics

All models are evaluated using the same set of metrics for fair comparison:

| Metric | What it measures | Target |
|---|---|---|

### Hyperparameter tuning

XGBoost is tuned using ___.

### Experiment tracking

All model runs are logged to MLflow.

---

## Setup instructions

### 1. Clone the repository

```bash

```

### 2. Create and activate a conda environment

```bash

```

### 3. Install dependencies

```bash

```

### 4. Add the data file

Place `timeseries_with_features.csv` inside the `data/` folder.
This file is produced by `W1-Feature_Engineering.ipynb`.

### 5. Run the notebooks in order

```
W3-mlflow.ipynb 
W3-streamlit.ipynb  
```

### 6. Launch the Streamlit app

Open Anaconda Prompt and run:

```bash

```

Then open **http://localhost:8501** in your browser.

---

## How to use the app

1. 
2. 
3. 
4. 
5. 

---

## Author and contact

**Name:** 
**Cohort:**
**GitHub:** 
**Email:** 
**Date completed:**
