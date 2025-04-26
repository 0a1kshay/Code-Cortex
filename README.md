# 🚀 Spacecraft Telemetry Anomaly Detection System

This project is a complete system designed to *detect anomalies in spacecraft telemetry data* using CSV or real-time sensor input. It provides interactive visualizations, anomaly flagging, and log-based UI for reviewing data.

---

## 👥 Team Details

- *Team Name:* CODE CORTEX
- *Team ID:* 03

---

## ⚙ Features

- 📈 *Streamlit GUI* for uploading CSV or live reading
- 🔴 *Anomaly Detection* using user-defined thresholds
- 📊 *Interactive Graphs* with Plotly + Matplotlib
- 🧪 *Real-time Simulation* with sockets
- 📁 *Log Viewer UI* built with Tkinter
- 🔄 *Multi-process launcher* to start everything at once

---

## 🧠 Libraries Used

- streamlit, pandas, matplotlib, plotly
- tkinter, socket, subprocess, signal
- datetime, zoneinfo, random, os, time

---

## ▶ Getting Started

### 1. Clone the Repository
bash
git clone https://github.com/your-username/spacecraft-telemetry-analyzer.git
cd spacecraft-telemetry-analyzer


### 2. Install Dependencies
bash
pip install -r requirements.txt


### 3. Run the App (CSV Analysis)
bash
streamlit run main_gui.py


### 4. Run the Live Telemetry System
bash
python run_telemetry_app.py


---

## 📥 Input Files

- telemetry.csv – Sample input CSV telemetry data file.
- anomalies.txt – Text file that records detected anomalies.

---

## 📌 Future Scope
- ML-based anomaly detection
- Email/SMS alert system
- Real spacecraft sensor integration

---
