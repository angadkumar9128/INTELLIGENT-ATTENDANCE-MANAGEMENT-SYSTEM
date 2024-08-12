import face_recognition
import cv2
import os
from datetime import datetime

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the directory where the images are stored
images_directory = os.path.join(current_directory, 'images_01')

# Replace these with your own data or more student details
KNOWN_FACES = {
    "Akshay": os.path.join(images_directory, 'Akshay.jpeg'),
    "Angad kumar": os.path.join(images_directory, 'angad.jpg'),
    "Jackie Shroff": os.path.join(images_directory, 'jacki.jpg'),
    # Add more faces with their corresponding image paths
}

def load_known_faces():
    # Initialize an empty dictionary to store the encodings of known faces
    known_encodings = {}

    # Iterate over each name and corresponding image path in the KNOWN_FACES dictionary
    for name, image_path in KNOWN_FACES.items():
        # Load the image from the specified file path
        image = face_recognition.load_image_file(image_path)
        # Generate the face encoding for the loaded image (assuming there's only one face per image)
        encoding = face_recognition.face_encodings(image)[0]
        # Store the face encoding in the known_encodings dictionary with the person's name as the key
        known_encodings[name] = encoding
    
    # Return the dictionary containing the face encodings of all known individuals
    return known_encodings

def mark_attendance(name):
    # Define the path to the attendance file within the current directory
    attendance_file = os.path.join(current_directory, "attendance.txt")
    # Get today's date to ensure attendance is marked only once per day
    today = datetime.now().date()

    # (Additional code will follow here in the actual function to handle marking attendance)


    # Read the attendance file to check if the user has already been marked present today
    with open(attendance_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if name in line and str(today) in line:
                return  # Already marked for today, exit function

    # Mark attendance with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(attendance_file, "a") as file:
        file.write(f"{name}, {timestamp}, present\n")


def recognize_faces(frame, face_locations, face_encodings, known_encodings, tolerance=0.6):
    # Iterate over each face encoding found in the frame
    for face_encoding in face_encodings:
        # Compare the current face encoding with known encodings to find matches
        matches = face_recognition.compare_faces(list(known_encodings.values()), face_encoding, tolerance=tolerance)
        name = "Unknown"  # Default name if no match is found

        # Check if there's a match
        if True in matches:
            # Find the index of the first match
            matched_index = matches.index(True)
            # Retrieve the corresponding name using the index
            name = list(known_encodings.keys())[matched_index]

        # Draw a rectangle around each detected face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Put the name label just below the rectangle
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        # If a known face is recognized, mark attendance
        if name != "Unknown":
            mark_attendance(name)

def main():
    # Initialize video capture from the default camera (usually webcam)
    video_capture = cv2.VideoCapture(0)
    # Load known face encodings
    known_encodings = load_known_faces()

    while True:
        # Capture a frame from the video
        ret, frame = video_capture.read()
        # Resize the frame for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Detect face locations and their encodings in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Recognize faces in the frame
        recognize_faces(frame, face_locations, face_encodings, known_encodings)

        # Display the video with the rectangles and labels
        cv2.imshow('Video', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the display window
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
