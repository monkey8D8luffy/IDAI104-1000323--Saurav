# 🚀 Aerospace Command Terminal: Rocket Launch Path Visualization

**Repository Name:** IDAI104-1000323--Saurav
**Live Streamlit Web App:** https://idai104-1000323--saurav-dds7mwphzyuhupyzghkbws.streamlit.app/

---

## 📌 Project Overview
[cite_start]The Aerospace Command Terminal is an advanced Streamlit cloud web app that focuses on visualizing and comparing different aspects of rocket launches. [cite_start]By combining mathematical flight simulations with historical real-world mission data, the project showcases clear insights into how resources, costs, and outcomes vary across different space missions. 

[cite_start]The primary goal of this web app is to create interactive visualizations that help users—such as engineers and data analysts—easily explore how factors like fuel consumption, payload weight, mission cost, and success rates connect with each other. [cite_start]Additionally, it features a dynamic 3D physics simulator that applies mathematical models covering calculus and differential equations to simulate real aerospace systems.

---

## ✨ Key Features & What the App Visualizes
This application is divided into two core modules:

### 1. Mission Data Intelligence (Exploratory Data Analysis)
[cite_start]This module analyzes the provided `.csv` dataset of past space missions. It features:
* **Interactive Dashboards:** Utilizing Plotly to visualize the mass-to-propellant ratio (Payload vs. Fuel) and aggregate financial expenditures based on mission success.
* [cite_start]**Core Statistical Distributions:** Utilizing Matplotlib and Seaborn to plot statistical variance, including crew size distributions and mean capital expenditure per mission[cite: 82, 88, 89].
* **Multi-Dimensional Analytics:** A 3D parameter space map and a Pearson correlation matrix that mathematically identify the strongest relationships between telemetry variables.

### 2. Advanced Flight Physics Simulator
A custom-built mathematical simulation engine that calculates rocket trajectories in real-time.
* [cite_start]**Differential Equations:** Calculates acceleration as the difference between upward thrust and downward forces (gravity and aerodynamic drag), divided by the rocket's dynamic mass[cite: 61].
* [cite_start]**Step-by-Step Integration:** At each time step, the loop updates velocity from acceleration and altitude from velocity[cite: 62].
* **Real-Time 3D Rendering:** Generates a live 3D orbital trajectory path and a 2D ascent profile based on the computed kinematics.

---

## ⚙️ Integration Details
[cite_start]This project integrates several industry-standard Python libraries to process data and render the UI[cite: 184]:
* **Streamlit:** Serves as the core web framework, utilizing custom CSS for a highly optimized, "Clear Glassmorphism" aerospace theme.
* [cite_start]**Pandas:** Used to load the dataset, clean the data (handling missing values, converting date formats), and ensure numeric columns are processed correctly[cite: 41, 42, 46, 47, 49].
* **NumPy:** Powers the numerical integration, logarithmic calculations (Tsiolkovsky rocket equation), and trigonometric vectoring for the 3D physics engine.
* [cite_start]**Plotly, Matplotlib, & Seaborn:** Integrated to create both highly interactive (hoverable/animated) and mathematically static data visualizations[cite: 82].

---

## 🚀 Deployment Instructions

### Prerequisites
Ensure you have Python installed on your local machine. [cite_start]The required libraries are listed in the `requirements.txt` file. 

### Running the App Locally
1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
