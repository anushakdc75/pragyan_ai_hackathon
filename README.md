# Pragyan_ai_hackathon
# Smart Air Quality Intelligence Platform

## AI-Powered Pollution Analytics for Smart Cities

The **Smart Air Quality Intelligence Platform** is an advanced AI-driven system designed to **monitor, analyze, and predict Air Quality Index (AQI)** using machine learning and real-time pollution data.

This platform helps governments, researchers, and citizens **understand pollution trends, predict future air quality, and make data-driven environmental decisions**.


# Key Innovation

Most AQI systems only show **current pollution levels**.

Our platform goes further by combining:

* **Machine Learning Prediction**
* **Real-time Pollution API**
* **Explainable AI**
* **Future AQI Forecasting**
* **Interactive Smart-City Dashboards**

This transforms raw pollution data into **actionable environmental intelligence**.


# Hackathon Problem Solved

Air pollution is one of the **largest environmental threats to human health**, causing:

* Respiratory diseases
* Reduced life expectancy
* Environmental degradation

However, most systems lack:

1 Predictive intelligence
2 Explainable insights
3 Visual analytics

Our platform solves this by providing:

✅ Predictive pollution analytics
✅ Interactive dashboards
✅ Real-time monitoring
✅ AI-driven insights


#  Core Features

##  Live AQI Monitoring

Fetches real-time pollution data using the **World Air Quality Index API**.

Displays:

* PM2.5
* PM10
* NO₂
* CO
* Ozone
* AQI

Users can instantly see **current pollution conditions** in selected cities.


##  Machine Learning AQI Prediction

The system predicts AQI using a trained **XGBoost regression model** based on pollutant concentrations.

Model Inputs:

* PM2.5
* PM10
* NO
* NO₂
* NH3
* CO
* SO₂
* O₃
* Benzene
* Toluene
* Xylene
* Temporal features (month, day, weekday)

The model generates an **AI-based AQI estimate** with pollution category classification.


##  Smart Pollution Dashboard

Interactive visual analytics built with Plotly:

* AQI trend analysis
* PM2.5 vs AQI correlation
* Pollution distribution
* City pollution patterns

These dashboards help identify **pollution drivers and patterns**.



##  Multi-City Pollution Comparison

Compare pollution levels across multiple cities simultaneously.

Features:

* Time-series AQI comparison
* Trend detection
* Cross-city pollution insights

This enables **regional environmental analysis**.


##  Future AQI Forecasting

Using **Facebook Prophet time-series forecasting**, the platform predicts **future air quality trends**.

Capabilities:

* Predict next 30 days AQI
* Identify pollution spikes
* Anticipate environmental risks

This supports **proactive pollution management**.


##  Explainable AI (XAI)

Machine learning models are often black boxes.

This system uses **SHAP Explainability** to reveal:

* Which pollutants affect AQI most
* Feature importance
* Model decision transparency

This builds **trust and interpretability in AI predictions**.



##  Interactive Pollution Map

A dynamic geospatial visualization that displays:

* City-level AQI bubbles
* Pollution intensity through color gradients
* AQI-based bubble sizing

This allows users to **visualize pollution hotspots across India**.


#  Advanced UI/UX

The platform is designed with **modern dashboard aesthetics**:

* Dark SaaS-style interface
* Glassmorphism metric cards
* AQI hero card visualization
* Gauge-style AQI meter
* Interactive charts
* Gradient AQI scale

Inspired by professional analytics dashboards used by:

* Environmental agencies
* Smart-city platforms
* Climate monitoring tools


#  AI & Data Science Stack

Machine Learning:

* XGBoost Regression

Explainable AI:

* SHAP

Forecasting:

* Facebook Prophet

Data Processing:

* Pandas
* NumPy

Visualization:

* Plotly
* Folium
* Streamlit


#  System Architecture

```
Pollution Dataset
        │
        ▼
Data Preprocessing
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Model (XGBoost)
        │
        ▼
Prediction + Explainable AI
        │
        ▼
Interactive Dashboard (Streamlit)
        │
        ▼
Real-Time AQI API Integration
```


#  Project Structure

```
AQI_SMART_PLATFORM
│
├── app.py
├── aqi_model.pkl
├── city_encoder.pkl
├── city_day.csv
├── requirements.txt
└── README.md
```


#  Deployment

The application can be deployed easily using:

* GitHub
* Streamlit Cloud

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```


# Impact

This platform enables:

* Smart-city pollution monitoring
* Predictive environmental intelligence
* Public awareness about air quality
* Data-driven policy decisions

Potential users:

* Environmental agencies
* Smart city planners
* Climate researchers
* Citizens concerned about air quality


#  Future Improvements

Potential extensions include:

* Satellite pollution data integration
* IoT air-quality sensors
* Deep learning pollution forecasting
* Mobile app integration
* AI-based health risk alerts

# Author

Developed as part of a **Data Science & AI Project** focused on building intelligent systems for environmental sustainability.

#  If you like this project

Please consider **starring the repository** to support the work!
