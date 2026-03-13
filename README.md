# 🚀 Aerospace Data Insights - Space Mission 

## 📌 Project Overview
This project involves a Streamlit cloud web app designed for **Aerospace Data Insights**. It provides a hands-on experience visualizing space missions and simulating a rocket launch using differential equations and real-world math formulas. 

The dashboard enables users (like engineers and building managers) to explore various scenarios, making insights accessible regarding payload limits, fuel consumptions, mission costs, and success rates.

## 📊 Features & Visualizations
- **Data Filtering:** Filter by Mission Type, Launch Vehicle, and Launch Year using Streamlit sidebars.
- **Custom Rocket Loading Animation** using CSS and Streamlit-Lottie.
- **Visuals Included:**
  1. Scatter Plot (Plotly): Payload Weight vs Fuel Consumption.
  2. Bar Chart (Plotly): Mission Cost split by Success/Failure.
  3. Line Chart (Seaborn): Mission Duration vs Distance from Earth.
  4. Box Plot (Seaborn): Crew Size vs Outcome Distribution.
  5. Scatter Plot (Plotly): Scientific Yield vs Mission Cost.
- **Rocket Physics Simulation Engine:** Uses Python loops to simulate differential equations adjusting thrust, gravity, atmospheric drag, and mass reduction over time, plotting live altitude.

## 🔗 Live Streamlit Web App
https://idai104-1000323--saurav-dds7mwphzyuhupyzghkbws.streamlit.app/


## ⚙️ How to Deploy & Run Locally

### Run Locally
1. Clone this repository.
2. Install necessary dependencies:
   ```bash
   pip install -r requirements.txt
