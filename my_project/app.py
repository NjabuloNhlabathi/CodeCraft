from flask import Flask, render_template
import serial

app = Flask(__name__)

import threading
import time
import serial

# Global variables to store the latest sensor data
latest_distance = 'Waiting for connection...'
latest_gas = 'Waiting for connection...'

def read_serial():
    global latest_distance, latest_gas
    ser = None

    while True:
        # If not connected, try to connect
        if ser is None or not ser.is_open:
            latest_distance = 'COM Port Blocked/Disconnected'
            latest_gas = 'COM Port Blocked/Disconnected'
            try:
                ser = serial.Serial('COM3', 9600, timeout=1)
                print("Successfully connected to COM3")
                latest_distance = 'Connected! Waiting for data...'
                latest_gas = 'Connected! Waiting for data...'
            except serial.SerialException:
                time.sleep(2) # Wait before retrying
                continue

        # If connected, try to read data
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if 'Distance:' in line:
                    parts = line.split('|')
                    latest_distance = parts[0].replace('Distance:', '').strip()
                    if len(parts) > 1:
                        latest_gas = parts[1].replace('Gas Level:', '').strip()
            else:
                time.sleep(0.1) # Small sleep to prevent CPU hogging
        except Exception as e:
            print(f"Serial error/disconnected: {e}")
            ser.close()
            ser = None

# Start the background thread for reading serial data
threading.Thread(target=read_serial, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', distance=latest_distance, gas=latest_gas)

if __name__ == '__main__':
  app.run(debug=True, port=5000, use_reloader=False)