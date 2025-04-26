import tkinter as tk
from tkinter import ttk
import os

LOG_FILE = "live_anomalies_log.txt"

class AnomalyViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚀 Spacecraft Telemetry Anomaly Viewer")
        self.geometry("800x400")
        self.configure(bg="#0e101a")

        style = ttk.Style(self)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), foreground="#ffffff", background="#333")
        style.map("Treeview", background=[("selected", "#4455aa")])

        self.tree = ttk.Treeview(self, columns=("timestamp", "sensor", "temperature", "pressure"), show='headings')
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("sensor", text="Sensor ID")
        self.tree.heading("temperature", text="Temperature (°C)")
        self.tree.heading("pressure", text="Pressure (bar)")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        refresh_btn = tk.Button(self, text="🔄 Refresh Now", command=self.load_anomalies, bg="#3a3f4b", fg="white", font=("Segoe UI", 10, "bold"))
        refresh_btn.pack(pady=(0, 10))

        self.after(3000, self.auto_refresh)  # refresh every 3 seconds
        self.load_anomalies()

    def load_anomalies(self):
        if not os.path.exists(LOG_FILE):
            return

        self.tree.delete(*self.tree.get_children())
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            if lines[i].startswith("Timestamp:"):
                timestamp = lines[i].split(":", 1)[1].strip()
                sensor_id = lines[i+1].split(":", 1)[1].strip()
                temperature = lines[i+2].split(":", 1)[1].strip()
                pressure = lines[i+3].split(":", 1)[1].strip()
                self.tree.insert("", "end", values=(timestamp, sensor_id, temperature, pressure))
                i += 4
            else:
                i += 1

    def auto_refresh(self):
        self.load_anomalies()
        self.after(3000, self.auto_refresh)
# gui.py

# Keep everything the same...

def run_gui():
    app = AnomalyViewer()
    app.mainloop()

if __name__ == "__main__":
    app = AnomalyViewer()
    app.mainloop()