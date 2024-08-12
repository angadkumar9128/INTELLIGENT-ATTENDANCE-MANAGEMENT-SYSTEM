import face_recognition  # Import face recognition library for face detection and encoding
import cv2  # Import OpenCV for video capture and image processing
import numpy as np  # Import NumPy for numerical operations
import os  # Import OS module for interacting with the operating system
from xlwt import Workbook  # Import Workbook from xlwt to create Excel files
from datetime import datetime, timedelta  # Import datetime and timedelta for handling dates and times
import xlrd  # Import xlrd for reading Excel files
from xlutils.copy import copy as xl_copy  # Import copy function to copy and modify existing Excel files

# Specify the folder containing the images for face recognition
image_folder = 'images_02'

# Get a reference to the webcam (usually webcam 0 is the default one)
video_capture = cv2.VideoCapture(0)

# Load all images from the specified folder and create face encodings for them
known_face_encodings = []  # Initialize an empty list to store face encodings
known_face_names = []  # Initialize an empty list to store corresponding names

# Loop through each file in the image folder
for file_name in os.listdir(image_folder):
    if file_name.endswith(('png', 'jpg', 'jpeg')):  # Check if the file is an image
        person_name = os.path.splitext(file_name)[0]  # Use the file name (without extension) as the person's name
        image_path = os.path.join(image_folder, file_name)  # Get the full path of the image file
        person_image = face_recognition.load_image_file(image_path)  # Load the image using face_recognition
        person_face_encoding = face_recognition.face_encodings(person_image)[0]  # Get the face encoding of the image
        known_face_encodings.append(person_face_encoding)  # Add the face encoding to the list
        known_face_names.append(person_name)  # Add the person's name to the list

# Initialize variables for face recognition process
face_locations = []  # List to store the locations of detected faces
face_encodings = []  # List to store the face encodings of detected faces
face_names = []  # List to store the names of detected faces
process_this_frame = True  # Variable to control processing every other frame for efficiency

# Initialize Excel workbook and sheet for storing attendance data
excel_file = 'Smart_Attendenance_Management_System_Project_02/attendance_excel.xls'
if not os.path.exists(excel_file):  # Check if the Excel file does not exist
    wb = Workbook()  # Create a new workbook
    wb.add_sheet('Sheet1')  # Add a default sheet to the workbook
    wb.save(excel_file)  # Save the new workbook to the specified file

rb = xlrd.open_workbook(excel_file, formatting_info=False)  # Open the existing Excel file for reading
wb = xl_copy(rb)  # Create a writable copy of the workbook
inp = input('Please give the current subject lecture name: ')  # Ask the user for the lecture name
sheet1 = wb.add_sheet(inp)  # Add a new sheet to the workbook with the given lecture name
sheet1.write(0, 0, 'Name')  # Write "Name" in the first cell of the first column
sheet1.write(0, 1, 'Status')  # Write "Status" in the first cell of the second column
sheet1.write(0, 2, 'Timestamp')  # Write "Timestamp" in the first cell of the third column
sheet1.write(0, 3, 'Attendance Count')  # Write "Attendance Count" in the first cell of the fourth column
row = 1  # Start writing data from the second row

attendance_records = {}  # Dictionary to store attendance data for each person

while True:  # Start an infinite loop to continuously capture video frames
    # Capture a single frame of video from the webcam
    ret, frame = video_capture.read()

    # Resize the captured frame to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the resized frame from BGR color (used by OpenCV) to RGB color (used by face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Detect all faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []  # Clear the list of face names for this frame
        for face_encoding in face_encodings:  # Loop through each detected face
            # Compare the detected face with the known faces to find a match
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"  # Default name is "Unknown" if no match is found

            # Use the known face with the smallest distance (i.e., closest match) to the detected face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:  # If a match is found
                name = known_face_names[best_match_index]  # Get the corresponding name

            face_names.append(name)  # Add the detected name to the list
            current_time = datetime.now()  # Get the current date and time

            if name != "Unknown":  # If a known person is detected
                if name in attendance_records:  # Check if this person has been detected before
                    last_entry = attendance_records[name]  # Get the last recorded entry for this person
                    last_status = last_entry['status']  # Get the last recorded status (Punch In or Punch Out)
                    last_time = last_entry['time']  # Get the last recorded time
                    attendance_count = last_entry['attendance_count']  # Get the last recorded attendance count

                    # If the last status was "Punch In" and 8 hours have passed since then
                    if last_status == "Punch In" and current_time - last_time >= timedelta(hours=8):
                        status = "Punch Out"  # Set the current status to "Punch Out"
                        attendance_count += 1  # Increase the attendance count by 1
                        # Update the attendance record for this person
                        attendance_records[name] = {'status': status, 'time': current_time, 'attendance_count': attendance_count}

                        # Write the updated information to the Excel sheet
                        sheet1.write(row, 0, name)  # Write the person's name
                        sheet1.write(row, 1, status)  # Write the current status
                        sheet1.write(row, 2, current_time.strftime('%Y-%m-%d %H:%M:%S'))  # Write the current timestamp
                        sheet1.write(row, 3, attendance_count)  # Write the updated attendance count
                        row += 1  # Move to the next row for the next entry
                        
                        print(f"Punch Out recorded for {name}. Attendance Count: {attendance_count}")
                    # If the last status was "Punch Out" or the last "Punch In" was within 8 hours
                    elif last_status == "Punch Out" or (last_status == "Punch In" and current_time - last_time < timedelta(hours=8)):
                        print(f"{name} cannot punch in/out again within 8 hours.")
                        continue  # Skip the rest of the loop for this person
                    # If the last status was "Punch Out" and 8 hours have passed
                    elif last_status == "Punch Out" and current_time - last_time >= timedelta(hours=8):
                        status = "Punch In"  # Set the current status to "Punch In"
                        # Update the attendance record for this person
                        attendance_records[name] = {'status': status, 'time': current_time, 'attendance_count': attendance_count}

                        # Write the updated information to the Excel sheet
                        sheet1.write(row, 0, name)  # Write the person's name
                        sheet1.write(row, 1, status)  # Write the current status
                        sheet1.write(row, 2, current_time.strftime('%Y-%m-%d %H:%M:%S'))  # Write the current timestamp
                        sheet1.write(row, 3, attendance_count)  # Write the attendance count
                        row += 1  # Move to the next row for the next entry

                        print(f"Punch In recorded for {name}. Attendance Count: {attendance_count}")
                else:
                    # If this person is being recorded for the first time
                    status = "Punch In"  # Set the current status to "Punch In"
                    # Create a new attendance record for this person
                    attendance_records[name] = {'status': status, 'time': current_time, 'attendance_count': 1}

                    # Write the new information to the Excel sheet
                    sheet1.write(row, 0, name)  # Write the person's name
                    sheet1.write(row, 1, status)  # Write the current status
                    sheet1.write(row, 2, current_time.strftime('%Y-%m-%d %H:%M:%S'))  # Write the current timestamp
                    sheet1.write(row, 3, 1)  # Write the initial attendance count (1)
                    row += 1  # Move to the next row for the next entry

                    print(f"Punch In recorded for {name}. Attendance Count: 1")

        wb.save(excel_file)  # Save the Excel file after each update

    process_this_frame = not process_this_frame  # Alternate between processing and skipping frames

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Data saved. Exiting...")
        break

# Release the webcam and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
