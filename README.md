# M.I.M.I. — Multitier IoT Machine Interaction

> **1st Place Winner — MICT SETA Regional Hackathon (Mpumalanga)**  
> An autonomous edge-to-cloud IoT submarine prototype designed for hazardous underwater environmental monitoring, gas detection, and remote water sampling.

---

## Overview

Inspecting contaminated, confined, or hazardous water bodies puts human divers at risk and delays water-quality testing. **M.I.M.I. (Multitier IoT Machine Interaction)** addresses this with a compact, 3D-printed autonomous underwater vehicle (AUV) that navigates submerged environments, streams live telemetry, and collects physical water samples on command.

### Key Capabilities
- **Obstacle Detection & Navigation:** Ultrasonic sensing for real-time distance measurement and collision avoidance.
- **Hazardous Gas Monitoring:** Onboard gas sensors to detect dangerous atmospheric or surface-level emissions near industrial and mining water sources.
- **Remote Water Sampling:** Actuated water-sampling pump to collect liquid samples from target zones for laboratory analysis.
- **Edge-to-Cloud Dashboard:** Web-based monitoring interface (`Index.html` / `my_project/`) for live sensor telemetry, alerts, and system control.
- **Custom 3D-Printed Hull:** Hydrodynamic enclosure modeled in Autodesk Fusion (`3D model/`) to house electronics and ballast securely.

---

## Repository Structure

```text
CodeCraft/
├── 3D model/        # Autodesk Fusion CAD files and printable STL parts for the submarine hull
├── firmware/        # Microcontroller source code (sensor polling, motor/pump actuation, telemetry)
├── media/           # Prototype photos, test run videos, and hardware demos
├── my_project/      # Backend application / Flask server and telemetry handling
├── powerpoint/      # Hackathon pitch deck and architecture presentation slides
├── simulation/      # Circuit schematics and pre-deployment hardware simulations
├── Index.html       # Frontend monitoring dashboard interface
├── style.css        # Dashboard styling
└── README.md        # Project documentation


[Ultrasonic & Gas Sensors] ──┐
                             ├──► [Microcontroller (Firmware)] ──► [Backend / Flask Server] ──► [Web Dashboard]
[Water-Sampling Pump] ◄──────┘

Perception & Actuation Layer (firmware/): Reads ultrasonic distance and gas concentration data while controlling propulsion and the water-sampling pump.

Simulation & Testing (simulation/): Validates sensor wiring, logic thresholds, and power distribution prior to physical assembly.

Application & Dashboard Layer (my_project/, Index.html, style.css): Receives telemetry packets, logs environmental readings, and exposes a browser-based operator interface.

Mechanical Enclosure (3D model/): Custom watertight housing engineered for modular component access and buoyancy balance.

Getting Started
Prerequisites
Hardware: Microcontroller (Arduino / ESP32), ultrasonic sensor, gas sensor module, DC water-sampling pump, jumper wires, and power supply.

Software:

Arduino IDE (or PlatformIO) for flashing firmware

Python 3.9+ (for running the backend server in my_project/)

Autodesk Fusion (optional, to inspect or modify files in 3D model/)

1. Clone the Repository
Bash
git clone [https://github.com/NjabuloNhlabathi/CodeCraft.git](https://github.com/NjabuloNhlabathi/CodeCraft.git)
cd CodeCraft
2. Flash the Firmware
Open the sketch inside firmware/ using the Arduino IDE.

Select your target board and COM port.

Verify the pin definitions match your wiring diagram in simulation/, then click Upload.

3. Run the Backend & Dashboard
Navigate to my_project/ and install any Python dependencies (e.g., pip install flask pyserial).

Start the local server:

Bash
cd my_project
python app.py
Open Index.html in your browser (or visit the local server URL shown in your terminal) to view live telemetry.

Future Roadmap
[ ] Add live underwater camera feed with computer vision turbidity/debris detection

[ ] Integrate GPS/acoustic waypoint logging for automated grid mapping

[ ] Standardize folder names (3D model -> 3d-model, my_project -> backend) and add automated tests

Author
Njabulo Nhlabathi

GitHub: @NjabuloNhlabathi

LinkedIn: Njabulo Nhlabathi


Before committing it, double-check the exact entry filename inside `my_project/` (listed above as `app.
