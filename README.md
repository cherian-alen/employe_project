

Project Overview
Employee Attendance System with Face Detection
This project aims to create an employee attendance system using Django for the backend, HTML/CSS/JavaScript for the frontend, and SQLite as the database. The system includes a face detection feature using OpenCV.

Technologies Used:
Backend: Python (Django)
Frontend: HTML, CSS, JavaScript
Database: SQLite
Machine Learning: OpenCV for face detection
Features:
Employees can log in using face detection.
Attendance records are stored securely in the database.
Admins can manage employee data and view attendance reports.
Installation Instructions
Clone this repository to your local machine:
git clone https://github.com/your-username/employee-attendance.git

Navigate to the project directory:
cd employee-attendance

Install Python dependencies:
pip install -r requirements.txt

Run database migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

Access the application in your web browser at http://localhost:8000.
Usage
Register employees in the system.
Capture employee faces for face recognition during registration.
Employees can log in by scanning their faces.
Admins can view attendance records and manage employee data.
