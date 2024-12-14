# [![TELEHIS Logo](https://imgur.com/RUjcwRS.png)](https://telehis.hacettepe.edu.tr/) : Remote Movement Tracking and Analysis System

## About the Project

This project aims to design a motion tracking system that can operate remotely to support the rehabilitation of individuals with **musculoskeletal disorders** (DMD - Duchenne Muscular Dystrophy, MS - Multiple Sclerosis, and lower back-neck issues).

- 2 **EMG** (Muscle Activity), 2 **FSR** (Pressure Sensors), and 2 **IMU** (Inertial Measurement Units) sensors are used to collect motion data.
- These data are processed by the **STM32** microcontroller and transmitted to a computer via **ESP32** over Wi-Fi.
- The data are analyzed using Python-based software and uploaded to AWS cloud systems (in the future, this data transfer will be moved to the official project website [telehis.hacettepe.edu.tr](https://telehis.hacettepe.edu.tr/)).

---

## Project Objectives

- To create a wearable and flexible rehabilitation system for individuals suffering from musculoskeletal disorders.
- To enable physiotherapists to remotely monitor patients and optimize treatment plans based on this data.
- To collect, process, and store motion data in cloud systems, creating a long-term archive for both patients and therapists.

---

## Hardware and Technologies Used

### Hardware

- **Sensors:**
  - 2 × EMG (Muscle activity sensors)
  - 2 × FSR (Pressure sensors)
  - 2 × IMU (Inertial measurement units)
- **Microcontrollers:**
  - **STM32:** Processing sensor data.
  - **ESP32:** Transmitting data to a computer over Wi-Fi.
- **Computer:** Analyzing data and transferring it to AWS.

### Software

- **Python**
  - Data analysis, motion detection, and AWS integration.
- **AWS Cloud Systems**
  - Temporary data storage and analysis platform.
- **Website (telehis.hacettepe.edu.tr)**
  - A future interface for patients and therapists where data will be transferred from AWS.

---

## Workflow

1. **Data Collection:** Collecting motion data from EMG, FSR, and IMU sensors using STM32.
2. **Data Transmission:** Transmitting data to a computer via ESP32 using Wi-Fi.
3. **Data Analysis:** Motion analysis and visualization using Python-based software.
4. **Data Storage:** Storing the data on AWS (to be moved to the website infrastructure in the future).

---

## Setup and Usage Instructions

### Setting Up Python Environment

1. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main file (e.g., `main.py`):
   ```bash
   python main.py
   ```

### STM32 and ESP32 Code

The necessary codes for STM32 and ESP32 can be found at the following GitHub repositories:

- **STM32 Codes:** [telehis-stm32](https://github.com/atilayilmaz/telehis-stm32)
- **ESP32 Codes:** [telehis-esp32](https://github.com/atilayilmaz/telehis-esp32)


