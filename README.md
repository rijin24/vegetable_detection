#  Vegetable Detector System

This repository contains the backend Flask server and the Android mobile application for vegetable recognition, recipe suggestions, and inventory checking.



## Table of Contents
- [Requirements](#requirements)  
- [Backend Setup (Flask Server)](#backend-setup-flask-server)  
- [Android App Setup](#android-app-setup)  
- [Running the System](#running-the-system)  
- [Notes](#notes)  

---

## ✅ Requirements

**System:** Ubuntu/Linux or Windows  
**Python:** 3.8+  
**Flask:** 2.x  
**MySQL:** 8.x  
**Android Studio:** Latest stable version  
**Java:** 11+  

### Python libraries:
pip install flask tensorflow flask-cors mysql-connector-python openpyxl pillow

Backend Setup (Flask Server)
1. Clone the Repository
git clone https://github.com/rijin24/vegetable_detection.git
cd vegetable_detection
2. Set up the Python Environment
(Optional but recommended)

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Configure MySQL Database
Create a database:

CREATE DATABASE store_db;


Make sure your config.py (or .env) has the correct credentials:

=
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'store_db'

4. Run the Flask Server

export FLASK_APP=app.py
export FLASK_ENV=development
flask run
By default, the server will run at:
http://127.0.0.1:5000/

You can test endpoints using Postman or your browser.

Android App Setup
1. Open Android Studio
Go to File > Open

Select the folder:

vegetable_detection/VegetableDetector2
2. Configure API URL and Network Security
Before building, update the IP address in two places:

go to > res/xml/network_security_config.xml

<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <!-- Replace with your machine's LAN IP -->
        <domain>192.168.0.157</domain>
    </domain-config>
</network-security-config>

go to > Constants.java

package com.example.vegetabledetector;

public class Constants {
    // Replace with your Flask server's IP and port
    public static final String BASE_URL = "http://192.168.0.157:5000/";
}


For Android emulator: use http://10.0.2.2:5000/

For physical device: use your PC’s local IP (check with ipconfig or ifconfig)

3. Build and Run
Connect a physical device or start an emulator.

Click Run ▶ in Android Studio.

The app will install and launch.

▶ Running the System
Start MySQL server.

Start the Flask backend (flask run).

Launch the Android app.

Capture a vegetable image in the app → prediction result is fetched from the server → recipes and store availability are displayed.

 Notes
Ensure both backend and Android app are on the same network if using a physical device.

For deployment on a cloud/VPS, update BASE_URL in Constants.java and <domain> in network_security_config.xml to your server’s public IP or domain.

Use HTTPS in production for secure communication.

Logs for Flask server will appear in the console; if running in background (Linux), check nohup.out or your process manager logs.
