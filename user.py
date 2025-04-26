# telemetry_user.py
import socket

TEMP_MIN = -40.0
TEMP_MAX = 85.0
PRESSURE_MIN = 0.8
PRESSURE_MAX = 1.5

def detect_anomaly(temp, pressure):
    temp_anomaly = not (TEMP_MIN <= temp <= TEMP_MAX)
    press_anomaly = not (PRESSURE_MIN <= pressure <= PRESSURE_MAX)
    return temp_anomaly, press_anomaly

def start_client(host='localhost', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"📥 Connected to Telemetry Server at {host}:{port}")

    with open("live_anomalies_log.txt", "w") as log:
        # Write CSV header
        log.write("timestamp,temperature,voltage,pressure\n")

        buffer = ""
        while True:
            data = client.recv(1024).decode()
            if not data:
                break
            buffer += data

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                try:
                    timestamp, sensor_id, temp, pressure = line.strip().split(",")
                    temp = float(temp)
                    pressure = float(pressure)
                    voltage = 28.0  # Simulated value (or modify as needed)

                    temp_anom, press_anom = detect_anomaly(temp, pressure)

                    # Always write the telemetry row
                    log.write(f"{timestamp},{temp},{voltage},{pressure}\n")
                    log.flush()

                    if temp_anom or press_anom:
                        print(f"⚠  Anomaly detected from {sensor_id} at {timestamp}")
                except Exception as e:
                    print(f"⚠ Failed to process line: {line} - {e}")

    client.close()

if __name__ == "__main__":
    start_client()
