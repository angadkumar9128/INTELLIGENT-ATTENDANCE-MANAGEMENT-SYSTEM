# Function to mark attendance
def mark_attendance(student_id):
    with open("attendance.txt", "a") as file:
        file.write(f"{student_id}, present\n")

# Function to view attendance
def view_attendance():
    with open("attendance.txt", "r") as file:
        attendance_records = file.readlines()
        for record in attendance_records:
            print(record.strip())

# Main function
def main():
    while True:
        print("\n--- Attendance Monitoring System ---")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            student_id = input("Enter Student ID: ")
            mark_attendance(student_id)
            print(f"Attendance marked for Student ID: {student_id}")
        elif choice == "2":
            print("\n--- Attendance Records ---")
            view_attendance()
        elif choice == "3":
            print("Exiting Attendance Monitoring System...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
