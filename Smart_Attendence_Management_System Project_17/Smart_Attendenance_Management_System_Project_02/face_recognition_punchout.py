import face_recognition
import cv2
import numpy as np
import os
from xlwt import Workbook
from datetime import datetime, timedelta
import xlrd
from xlutils.copy import copy as xl_copy

# Specify the folder containing the images
image_folder = 'images_02'

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load all the images and their encodings from the specified folder
known_face_encodings = []
known_face_names = []

for file_name in os.listdir(image_folder):
    if file_name.endswith(('png', 'jpg', 'jpeg')):  # Check for image files
        person_name = os.path.splitext(file_name)[0]  # Use the file name (without extension) as the person's name
        image_path = os.path.join(image_folder, file_name)
        person_image = face_recognition.load_image_file(image_path)
        person_face_encoding = face_recognition.face_encodings(person_image)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(person_name)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Initialize workbook and sheet for Excel file
excel_file = 'Smart_Attendenance_Management_System_Project_02/attendance_excel.xls'
if not os.path.exists(excel_file):
    wb = Workbook()
    wb.add_sheet('Sheet1')
    wb.save(excel_file)

rb = xlrd.open_workbook(excel_file, formatting_info=False)
wb = xl_copy(rb)
inp = input('Please give the current subject lecture name: ')
sheet1 = wb.add_sheet(inp)
sheet1.write(0, 0, 'Name')
sheet1.write(0, 1, 'Status')
sheet1.write(0, 2, 'Timestamp')
sheet1.write(0, 3, 'Attendance Count')
row = 1

attendance_records = {}

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            current_time = datetime.now()

            if name != "Unknown":
                if name in attendance_records:
                    last_entry = attendance_records[name]
                    last_status = last_entry['status']
                    last_time = last_entry['time']
                    attendance_count = last_entry['attendance_count']

                    if last_status == "Punch In" and current_time - last_time >= timedelta(hours=8):
                        status = "Punch Out"
                        attendance_count += 1
                        attendance_records[name] = {'status': status, 'time': current_time, 'attendance_count': attendance_count}

                        # Write to Excel file
                        sheet1.write(row, 0, name)
                        sheet1.write(row, 1, status)
                        sheet1.write(row, 2, current_time.strftime('%Y-%m-%d %H:%M:%S'))
                        sheet1.write(row, 3, attendance_count)
                        row += 1
                        
                        print(f"Punch Out recorded for {name}. Attendance Count: {attendance_count}")
                    elif last_status == "Punch Out" or (last_status == "Punch In" and current_time - last_time < timedelta(hours=8)):
                        print(f"{name} cannot punch in/out again within 8 hours.")
                        continue
                    elif last_status == "Punch Out" and current_time - last_time >= timedelta(hours=8):
                        status = "Punch In"
                        attendance_records[name] = {'status': status, 'time': current_time, 'attendance_count': attendance_count}

                        # Write to Excel file
                        sheet1.write(row, 0, name)
                        sheet1.write(row, 1, status)
                        sheet1.write(row, 2, current_time.strftime('%Y-%m-%d %H:%M:%S'))
                        sheet1.write(row, 3, attendance_count)
                        row += 1

                        print(f"Punch In recorded for {name}. Attendance Count: {attendance_count}")
                else:
                    status = "Punch In"
                    attendance_records[name] = {'status': status, 'time': current_time, 'attendance_count': 1}

                    # Write to Excel file
                    sheet1.write(row, 0, name)
                    sheet1.write(row, 1, status)
                    sheet1.write(row, 2, current_time.strftime('%Y-%m-%d %H:%M:%S'))
                    sheet1.write(row, 3, 1)
                    row += 1

                    print(f"Punch In recorded for {name}. Attendance Count: 1")

                wb.save(excel_file)
            else:
                print("Next student")

    process_this_frame = not process_this_frame

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

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Data saved and program terminated.")
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
