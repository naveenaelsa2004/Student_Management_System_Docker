# Student Management System

A beginner-friendly, dockerized web application for managing student records using Python Flask, SQLite, Bootstrap 5, and Docker.

---

## Project Description

The **Student Management System** is a lightweight CRUD (Create, Read, Update, Delete) web application that enables administrators and teachers to manage student information seamlessly. The application stores data in an SQLite database and is fully containerized using Docker, utilizing Docker volumes to ensure data persistence across container lifecycles.

---

## Technologies Used

- **Backend**: Python 3.11, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5 (CDN)
- **Containerization**: Docker, Docker Compose

---

## Features

- **Responsive Dashboard**: View all registered students in a clean Bootstrap table with an empty-state display when no records exist.
- **Form Validation**: Validates required fields, email formatting, and phone number length before saving.
- **Flash Alerts**: Real-time feedback notifications for create, update, and delete actions.
- **SQL Injection Protection**: Uses parameterized SQL queries (`?`) for safe database transactions.
- **Data Persistence**: Uses a named Docker volume (`student_data`) so database records persist even if the container is stopped or recreated.

---

## Project Structure

```text
StudentManagement/
│
├── app.py                   # Main Flask application with CRUD routes and SQLite logic
├── requirements.txt         # Python dependencies (Flask)
├── Dockerfile               # Docker build configuration
├── docker-compose.yml       # Docker Compose configuration with persistent volume
├── .dockerignore            # Files excluded from Docker image build
├── .gitignore               # Files excluded from Git tracking
│
├── templates/               # HTML Jinja2 templates
│   ├── index.html           # Dashboard displaying student records
│   ├── add_student.html     # Form for registering a new student
│   └── edit_student.html    # Form for updating an existing student
│
├── static/                  # Static assets
│   └── style.css            # Custom CSS styles
│
└── README.md                # Project documentation
```

---

## CRUD Operations Explanation

- **Create (Add Student)**: Access `/add` to register a new student with Name, Email, Course, and Phone number. Input is validated and securely inserted into the database.
- **Read (View Students)**: The root route `/` fetches and displays all students in descending order of ID.
- **Update (Edit Student)**: Access `/edit/<id>` to view pre-populated student information and update details safely.
- **Delete (Remove Student)**: Submits a POST request to `/delete/<id>` with a JavaScript confirmation dialog to prevent accidental deletion.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Git](https://git-scm.com/) (optional, for cloning the repository).

---

## How to Build and Run with Docker

### Option 1: Using Standard Docker Commands

1. **Clone the repository and enter the directory**:
   ```bash
   git clone https://github.com/naveenaelsa2004/Student_Management_System_Docker.git
   cd Student_Management_System_Docker
   ```

2. **Build the Docker Image**:
   ```bash
   docker build -t student-management-app .
   ```

3. **Run the Container with a Persistent Volume**:
   ```bash
   docker run -d -p 5000:5000 --name student_app -v student_data:/app/data student-management-app
   ```

---

### Option 2: Using Docker Compose (Recommended)

1. **Start the application**:
   ```bash
   docker compose up -d --build
   ```

---

## Access the Application

Once the container is running, open your web browser and go to:

👉 **[http://localhost:5000](http://localhost:5000)**

---

## How to Stop and Restart the Container

### Using Docker CLI:

- **Check container status**:
  ```bash
  docker ps
  ```

- **View application logs**:
  ```bash
  docker logs student_app
  ```

- **Stop the container**:
  ```bash
  docker stop student_app
  ```

- **Restart the container**:
  ```bash
  docker restart student_app
  ```

- **Start a stopped container**:
  ```bash
  docker start student_app
  ```

- **Remove the container**:
  ```bash
  docker rm -f student_app
  ```

### Using Docker Compose:

- **Stop the application**:
  ```bash
  docker compose stop
  ```

- **Restart the application**:
  ```bash
  docker compose restart
  ```

- **Stop and remove containers**:
  ```bash
  docker compose down
  ```

---

## Data Persistence Verification

The SQLite database file is stored in `/app/data/students.db` inside the container and mounted to the Docker volume `student_data`. 

To verify data persistence:
1. Add student records via the web interface.
2. Stop and remove the container (`docker rm -f student_app`).
3. Run a new container using the same volume (`-v student_data:/app/data`).
4. Revisit [http://localhost:5000](http://localhost:5000) — all your previously saved student records will still be there.
