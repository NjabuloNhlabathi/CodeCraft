import threading
import time

import serial
from flask import Flask, render_template

app = Flask(__name__)

# Global variables to store the latest sensor data
latest_distance = 'Waiting for connection...'
latest_gas = 'Waiting for connection...'
serial_port = 'COM3'

def read_serial():
    global latest_distance, latest_gas
    ser = None

    while True:
        # If not connected, try to connect
        if ser is None or not ser.is_open:
            latest_distance = f'{serial_port} disconnected'
            latest_gas = f'{serial_port} disconnected'
            try:
                ser = serial.Serial(serial_port, 9600, timeout=1)
                print(f"Successfully connected to {serial_port}")
                latest_distance = 'Connected! Waiting for data...'
                latest_gas = 'Connected! Waiting for data...'
            except serial.SerialException as error:
                if 'Access is denied' in str(error):
                    status = f'{serial_port} is in use - close Serial Monitor'
                    latest_distance = status
                    latest_gas = status
                print(f"Unable to connect to {serial_port}: {error}")
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
        except (serial.SerialException, OSError) as error:
            print(f"Serial error/disconnected: {error}")
            if ser is not None and ser.is_open:
                ser.close()
            ser = None

# Start the background thread for reading serial data
threading.Thread(target=read_serial, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', distance=latest_distance, gas=latest_gas)

if __name__ == '__main__':
  app.run(debug=True, port=5000, use_reloader=False)