from flask import Flask, render_template
import serial

app = Flask(__name__)

# Update 'COM3' to your Arduino's port
ser = serial.Serial('COM3', 9600, timeout=1)


@app.route('/')
def index():
  distance = 'Waiting...'
  gas = 'Waiting...'

  if ser.in_waiting > 0:
    line = ser.readline().decode('utf-8').strip()
    # Parses strings like "Distance: 15 cm | Gas Level: 200"
    if 'Distance:' in line:
      parts = line.split('|')
      distance = parts[0].replace('Distance:', '').strip()
      if len(parts) > 1:
        gas = parts[1].replace('Gas Level:', '').strip()

  return render_template('index.html', distance=distance, gas=gas)


if __name__ == '__main__':
  app.run(debug=True, port=5000)