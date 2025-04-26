# telemetry_server.py
import socket
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo  # Available in Python 3.9+


def generate_data():
    timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    sensor_id = f"SENSOR_{random.randint(1, 10):03d}"
    temperature = round(random.uniform(-60, 120), 2)
    pressure = round(random.uniform(0.3, 2.0), 2)
    return f"{timestamp},{sensor_id},{temperature},{pressure}"

def start_server(host='localhost', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"🚀 Telemetry Server running on {host}:{port}...")

    conn, addr = server.accept()
    print(f"📡 Connection from {addr}")

    try:
        while True:
            data = generate_data()
            conn.sendall((data + "\n").encode())
            print(f"📤 Sent: {data}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Server stopped.")
    finally:
        conn.close()
        server.close()

if __name__ == "__main__":
    start_server()