# run_telemetry_app.py
import subprocess
import time
import sys
import os
import signal

# Get the current directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build full paths
server_path = os.path.join(BASE_DIR, "server.py")
client_path = os.path.join(BASE_DIR, "user.py")
gui_command = "import gui; gui.run_gui()"

# Start the server
server_proc = subprocess.Popen([sys.executable, server_path])
print("✅ Server started")

time.sleep(1)

# Start the client
client_proc = subprocess.Popen([sys.executable, client_path])
print("✅ Client started")

time.sleep(1)

# Start the GUI
gui_proc = subprocess.Popen([sys.executable, "-c", gui_command], cwd=BASE_DIR)
print("✅ GUI started")

try:
    server_proc.wait()
    client_proc.wait()
    gui_proc.wait()
except KeyboardInterrupt:
    print("🛑 Terminating all processes...")
    for proc in [server_proc, client_proc, gui_proc]:
        if proc.poll() is None:
            os.kill(proc.pid, signal.SIGTERM)
