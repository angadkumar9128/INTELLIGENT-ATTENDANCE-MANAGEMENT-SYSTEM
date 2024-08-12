# INTELLIGENT ATTENDANCE MANAGEMENT SYSTEM

 This Python project implements a facial recognition-based attendance system using OpenCV and face_recognition libraries. It tracks "Punch In" and "Punch Out" times, ensuring that attendance is only registered once per day or after 8 hours. Attendance records are stored in an Excel file, with each entry including a timestamp and an updated attendance count.


# Overview

This project provides a facial recognition-based attendance management system. It uses Python with OpenCV and the face_recognition library to automatically track employee attendance based on facial recognition. The system records "Punch In" and "Punch Out" times, ensuring that each individual can only register attendance once per day or after 8 hours. The attendance data is stored in an Excel file, including timestamps and attendance counts.

# Features

Facial Recognition: Utilizes the face_recognition library to detect and identify faces in real-time using a webcam.

Real-Time Attendance Tracking: Records "Punch In" when a person is detected for the first time and "Punch Out" when they are detected again after 8 hours.

Attendance Count Management: Maintains an attendance count for each individual, increasing by 1 each time they "Punch Out" after a "Punch In."

Excel Data Storage: Logs attendance data, including name, status ("Punch In" or "Punch Out"), timestamp, and attendance count, in an Excel file for easy record-keeping.

No Duplicate Entries: Ensures that each individual’s attendance is recorded only once per day or shift, preventing duplicate entries within the same day.

# Requirements

To run this project, you will need:

Python 3.x: Ensure Python 3 is installed on your machine. Download Python

Libraries:

face_recognition: For detecting and encoding faces.

opencv-python: For video capture and image processing.

numpy: For numerical operations.

xlwt: For creating and writing Excel files.

xlrd: For reading Excel files.

xlutils: For copying and modifying existing Excel files.

You can install the required libraries using pip:

pip install face_recognition opencv-python numpy xlwt xlrd xlutils

# Installation

Clone the Repository:

git clone https://github.com/yourusername/your-repository.git

cd your-repository

Install Dependencies:

Install the required Python libraries:

pip install face_recognition opencv-python numpy xlwt xlrd xlutils

Prepare the Image Folder:

Ensure you have a folder named images_02 containing images of individuals. Each image file should be named according to the person’s name (e.g., john_doe.jpg). Place this folder in the same directory as the script.

# Usage

Run the Script:

Execute the Python script to start the attendance tracking system:

python your_script.py

Enter Lecture Name:

When prompted, enter the current subject lecture name or identifier. This name will be used as the sheet name in the Excel file to categorize attendance records.

Webcam Feed:

The script will open a webcam feed. The system will continuously process video frames to detect faces and manage attendance based on the detected faces.

Exiting the Script:

Press the 'q' key to exit the script. The attendance data will be saved to the Excel file before closing.

# How It Works

Face Detection and Encoding:

The script captures frames from the webcam.

Each frame is processed to detect faces and generate face encodings.

Face Comparison:

Detected faces are compared to known face encodings (loaded from images in the images_02 folder).

If a match is found, the person’s name is identified.

Attendance Tracking:

Punch In: When a face is detected for the first time, it is marked as "Punch In."

Punch Out: If the same face is detected again after 8 hours, it is marked as "Punch Out," and the attendance count is incremented.

Attendance Count: Each "Punch Out" increases the attendance count. If the same face appears after 8 hours or the next day, it records another "Punch In."

Data Logging:

Attendance records, including names, statuses, timestamps, and attendance counts, are written to an Excel file.

Data Storage: Attendance records, including names, statuses, timestamps, and attendance counts, are written to an Excel file.

# Examples OutPut

When a person is recognized and punches in, the script will log:

Name	Status	Timestamp	Attendance Count

Alice	Punch In	2024-08-13 09:00:00	1

If Alice punches out and returns after 8 hours:

Name	Status	Timestamp	Attendance Count

Alice	Punch Out	2024-08-13 17:00:00	1

If Alice returns the next day:

Name	Status	Timestamp	Attendance Count

Alice	Punch In	2024-08-14 09:00:00	2

# Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgements
face_recognition for facial recognition capabilities.
OpenCV for image processing and video capture.
xlwt and xlrd for handling Excel files.
