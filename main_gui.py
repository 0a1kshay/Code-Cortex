import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import os
import time


st.set_page_config(layout="wide")

# Default thresholds
default_thresholds = {
    "temperature": 100.0,
    "pressure": 1.5,
    "voltage": 32.0,
    "current": 15.0,
    "radiation": 0.005,
    "acceleration": 3.0,
    "humidity": 70.0,
    "fuel_level": 10.0,
    "coolant_level": 25.0,
    "gyroscope_drift": 0.05,
    "solar_panel_output": 100.0
}


st.title("🚀 Spacecraft Telemetry Anomaly Detector")
file_source = st.radio(
    "Select Data Source",
    options=["Upload CSV File", "Live Telemetry Log"],
    index=0,
    horizontal=True
)

if file_source == "Upload CSV File":
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        # Sensor selection
        sensors = list(default_thresholds.keys())
        selected_sensors = st.multiselect("Select sensors to monitor", options=sensors, default=sensors)

        # Threshold configuration
        st.subheader("Threshold Configuration")
        custom_thresholds = {}
        for sensor in selected_sensors:
            custom_thresholds[sensor] = st.number_input(f"{sensor} threshold", value=default_thresholds[sensor])



        # Anomaly detection
        st.subheader("⚠ Anomalies Detected")
        anomalies = []

        anomalies = []

        for i, row in df.iterrows():
            for sensor in selected_sensors:
                if sensor not in df.columns:
                    continue
                val = row[sensor]
                if val > custom_thresholds[sensor]:
                    anomalies.append((i, sensor, val))



        if anomalies:
            anomalies_df = pd.DataFrame(anomalies, columns=["Index", "Sensor", "Value"])
            st.dataframe(anomalies_df)

    # Create plain-text content
            txt_lines = ["Anomaly Report\n==============\n"]
            for idx, sensor, value in anomalies:
                txt_lines.append(f"Row {idx}: {sensor} = {value} [ANOMALY]")

            txt_content = "\n".join(txt_lines).encode("utf-8")

            st.download_button(
                label="📄 Download Anomalies (TXT)",
                data=txt_content,
                file_name="anomalies.txt",
                mime="text/plain"
            )
        else:
            st.info("No anomalies found.")


        # Visualizations
        st.subheader("📈 Telemetry Visualizations")
        for sensor in selected_sensors:
            if sensor not in df.columns:
                continue

            fig_line = px.line(df, y=sensor, title=f"{sensor} Line Chart")
            st.plotly_chart(fig_line, use_container_width=True)

            fig_bar = px.bar(df, y=sensor, title=f"{sensor} Bar Chart")
            st.plotly_chart(fig_bar, use_container_width=True)

            fig_area = px.area(df, y=sensor, title=f"{sensor} Area Chart")
            st.plotly_chart(fig_area, use_container_width=True)

        # Export full plot area
        st.subheader("📤 Export Charts")
        fig_all = plt.figure(figsize=(10, 6))
        for sensor in selected_sensors[:4]:  # Limit to 4 for readability
            if sensor in df.columns:
                plt.plot(df.index, df[sensor], label=sensor)
        plt.legend()
        plt.title("Overview of Selected Sensors")
        st.pyplot(fig_all)

        buf = BytesIO()
        fig_all.savefig(buf, format="png")
        st.download_button("📷 Download Visualization (PNG)", buf.getvalue(), "visualization.png", "image/png")
elif file_source == "Live Telemetry Log":
    import time

    log_path = os.path.join(os.getcwd(), "live_anomalies_log.txt")

    if not os.path.exists(log_path):
        st.error("Log file 'live_anomalies_log.txt' not found.")
    else:
        try:
            # Attempt to load the log file with proper columns
            df = pd.read_csv(log_path, names=["timestamp", "temperature", "voltage", "pressure"])
            st.success("Live telemetry log loaded!")

            st.subheader("📈 Live Telemetry Visualizations")

            sensors = [col for col in df.columns if col != "timestamp"]
            selected_sensors = st.multiselect("Select sensors to visualize", options=sensors, default=sensors)

            for sensor in selected_sensors:
                fig = px.line(df, x="timestamp", y=sensor, title=f"{sensor} Over Time")
                st.plotly_chart(fig, use_container_width=True)

            # Refresh every 5 seconds
            time.sleep(5)
            st.rerun()

        except Exception as e:
            st.error(f"Error reading the telemetry log: {e}")
