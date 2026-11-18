# CampusHub ERP

CampusHub ERP is a college management backend with a lightweight web dashboard and interactive API documentation.

## Dashboard and interface

After starting the application, open **http://127.0.0.1:8000/** to view the CampusHub overview dashboard. It displays live totals for students, faculty, courses, and enrollments, along with a recent-students table and quick links to the API explorer. The dashboard reads its information from the existing API endpoints; it does not replace or change the underlying CRUD operations.

Use **http://127.0.0.1:8000/docs** to access the interactive Swagger API documentation, where records can be created, viewed, updated, and deleted using the available endpoints.

*A lightweight college management REST API built with Python and FastAPI.*

CampusHub ERP is a Python-based college management backend for maintaining student, faculty, course and enrolment records in an SQLite database.

The project provides a REST API rather than a standalone college website or administration dashboard. You can explore and test its endpoints through the interactive Swagger UI documentation included with FastAPI.

## Key features

- Add, view, update and delete student records.
- Add, view, update and delete faculty records.
- Add, view, update and delete course records.
- Enrol a student in a course and view or remove enrolments.
- Store records in SQLite so they remain available after the server is stopped.
- Generate text reports for students, faculty and courses.
- Export database records to JSON files.
- Write application activity to a log file.

## Technology stack

- **Python** – application logic
- **FastAPI** – REST API
- **Uvicorn** – local development server
- **SQLAlchemy** – database access and ORM models
- **SQLite** – local database (`campushub.db`)
- **Pydantic** – request validation
- **Pytest** – automated tests

## Directory structure

```text
CampusHubERP/
├── app/
│   ├── api/              # HTTP routes for each management area
│   ├── core/             # Validation, descriptors, metaclasses and interfaces
│   ├── database/         # SQLite setup, ORM models and repository
│   ├── models/           # Domain models
│   ├── services/         # Student, faculty, course and enrolment logic
│   ├── utils/            # IDs, reports, logging, serialization and helpers
│   └── main.py           # FastAPI application and Swagger styling
├── data/                 # JSON data exports / import files
├── logs/                 # Application log
├── reports/              # Generated text reports
├── tests/                # Automated tests
├── campushub.db          # SQLite database with the supplied sample records
├── main.py               # Startup tasks and Uvicorn launch
├── requirements.txt
└── README.md
```

The student API and JSON file deliberately use the name `You` (`/You` and `data/You.json`) to retain the naming used in the project assignment. In the API documentation, this section is labelled **Students**.

## Prerequisites

- Windows 10/11 (the commands below use PowerShell)
- Python 3.10 or newer
- VS Code or another editor
- Internet access for the first installation, so Python packages can be downloaded

Python must be available from the terminal. On Windows, the `py` launcher is usually available with a standard Python installation.

## Setup on Windows

Clone or download the repository and open the `CampusHubERP` project folder in VS Code. Select **Terminal → New Terminal** to open a terminal at the project location.

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell refuses to run the activation script, allow it for the current terminal session and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Create the virtual environment and install dependencies only once for this project folder. In each new terminal session, activate the environment again before launching the application.

## Start the application

From the project root, with `.venv` activated, run:

```powershell
python main.py
```

The startup script initializes the database, loads the available records, generates reports, exports the database contents as JSON files and displays a record-count summary. It then launches the API server.

Open these addresses in your browser:

- API status: <http://127.0.0.1:8000/>
- Interactive API documentation: <http://127.0.0.1:8000/docs>

Keep the terminal running while you use the API. To stop the server, press `Ctrl + C` in the same terminal.

### Running it next time

You do not need to repeat the installation. Open the project folder in VS Code, open a new terminal and run:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

## Working with the API

The `/docs` page opens Swagger UI, an interactive API testing interface. It is not a graphical college administration dashboard.

Each expandable row represents an API endpoint. Open an endpoint, select **Try it out**, enter the required path parameters or JSON request body, and then select **Execute**. The response panel displays the HTTP status code along with the returned data or error details.

The four main sections are:

| Section in the docs | Route prefix | Purpose |
|---|---|---|
| Students | `/You` | Manage student records |
| Faculty | `/faculty` | Manage faculty records |
| Courses | `/courses` | Manage course records |
| Enrollments | `/enrollments` | Link students to courses |

### Endpoint reference

| Method | Endpoint | What it does |
|---|---|---|
| GET | `/You` | List students; optionally filter by department |
| POST | `/You` | Add a student |
| GET | `/You/{ident}` | Get one student by ID |
| PUT | `/You/{ident}` | Update fields on a student |
| DELETE | `/You/{ident}` | Delete a student if no enrolment prevents it |
| GET | `/faculty` | List faculty; optionally filter by department |
| POST | `/faculty` | Add a faculty member |
| GET | `/faculty/{ident}` | Get one faculty member by ID |
| PUT | `/faculty/{ident}` | Update fields on a faculty member |
| DELETE | `/faculty/{ident}` | Delete a faculty member |
| GET | `/courses` | List courses |
| POST | `/courses` | Add a course |
| GET | `/courses/{ident}` | Get one course by code |
| PUT | `/courses/{ident}` | Update fields on a course |
| DELETE | `/courses/{ident}` | Delete a course if no enrolment prevents it |
| GET | `/enrollments` | List enrolments |
| POST | `/enrollments` | Enrol a student in a course |
| DELETE | `/enrollments/{ident}` | Delete an enrolment by ID |

There is no individual-enrolment GET endpoint or enrolment PUT endpoint in the current API.

## Request fields and validation

The following fields are accepted by the current API. Field names in JSON are case-sensitive.

### Students — `POST /You`

```json
{
  "name": "Rahul Verma",
  "age": 21,
  "email": "rahul.verma@example.com",
  "department": "Computer Science"
}
```

| Field | Required? | Rule |
|---|---|---|
| `student_id` | No | Optional. If supplied, must match `ST` followed by at least three digits, e.g. `ST004`. Otherwise the application generates an ID. |
| `name` | Yes | Non-empty string |
| `age` | Yes | Integer from 16 through 80 |
| `email` | Yes | Must look like a valid email address; must be unique among student records |
| `department` | Yes | Non-empty string |

A student response includes `student_id`, `name`, `age`, `email`, `department`, `created_at` and `updated_at`. The student list also includes `name_upper`, an uppercase version of the name.

### Faculty — `POST /faculty`

```json
{
  "name": "Ananya Desai",
  "age": 35,
  "email": "ananya.desai@example.com",
  "department": "Computer Science"
}
```

| Field | Required? | Rule |
|---|---|---|
| `faculty_id` | No | Optional. If supplied, must match `FC` followed by at least three digits, e.g. `FC003`. Otherwise the application generates an ID. |
| `name` | Yes | Non-empty string |
| `age` | Yes | Integer from 16 through 80 |
| `email` | Yes | Must look like a valid email address; must be unique among student records |
| `department` | Yes | Non-empty string |

### Courses — `POST /courses`

```json
{
  "course_name": "Artificial Intelligence",
  "credits": 4
}
```

| Field | Required? | Rule |
|---|---|---|
| `course_code` | No | Optional. If supplied, must contain 2–5 uppercase letters followed by at least three digits, e.g. `AI101` or `CS101`. Otherwise the application generates a code. |
| `course_name` | Yes | Non-empty string |
| `credits` | Yes | Integer from 1 through 10 |

### Enrollments — `POST /enrollments`

```json
{
  "student_id": "ST001",
  "course_code": "IT101"
}
```

| Field | Required? | Rule |
|---|---|---|
| `enrollment_id` | No | Optional. If omitted, the application generates an ID. |
| `student_id` | Yes | Must match an existing student ID |
| `course_code` | Yes | Must match an existing course code |

The same student cannot be enrolled in the same course more than once. The database enforces this rule. An enrolment also cannot be created unless both the student and course already exist.

### Updating records

PUT requests use the same path ID as the GET and DELETE routes. The request body can contain only the fields being changed; you do not need to send the complete record.

For example, to change a student's department:

```json
{
  "department": "Information Technology"
}
```

The ID in the URL identifies the record and cannot be changed through the update request. For students and faculty, valid email format and age limits still apply. For courses, credits must remain between 1 and 10.

## ID formats and sample data

The application generates IDs using these prefixes:

| Record | Generated format | Examples in the supplied database |
|---|---|---|
| Student | `ST` + digits | `ST001`, `ST002`, `ST003` |
| Faculty | `FC` + digits | `FC001`, `FC002` |
| Course | `CS` + digits | `CS101`, `CS201`, `IT101` |
| Enrollment | `EN` + digits | `EN001`, `EN002`, `EN003` |

Generated numbers depend on the records already in the database. Always copy the actual ID returned by a successful POST request or retrieve it using the relevant GET endpoint. Do not assume the next ID will be a particular number.

The bundled database contains sample students, faculty, courses and enrolments. The JSON files in `data/` are exported copies; the normal startup script exports the database to these files. It does not automatically import JSON records into a new, empty database.

## Recommended first-time workflow

A typical way to try the system is:

1. Run `GET /You` and note an existing student ID.
2. Run `GET /courses` and note an existing course code.
3. Run `POST /enrollments` with those two values.
4. Run `GET /enrollments` and confirm the new enrolment appears.
5. Try creating a new student or course, then use the returned IDs for another enrolment.

For example, the sample database includes student `ST001` and course `IT101`, so this request can be used if that sample data is present:

```json
{
  "student_id": "ST001",
  "course_code": "IT101"
}
```

## Business rules and database behavior

- Student, faculty, course and enrolment primary IDs must be unique.
- Student email addresses must be unique among students, and faculty email addresses must be unique among faculty members. The current database schema does not enforce uniqueness across the two separate tables.
- An enrolment must reference an existing student and an existing course.
- A student-course pair can only appear once in the enrolment table.
- A student or course that is referenced by an enrolment cannot be deleted until the related enrolment is removed.
- Records are stored in `campushub.db`; stopping and restarting the server does not clear the database.
- The student and faculty list endpoints accept an optional `department` query parameter. The department filter is case-insensitive.

## HTTP response codes

| Code | Meaning | What to check |
|---|---|---|
| `200` | Request succeeded | The response body contains the requested data or result. |
| `201` | Record created | The response body contains the newly created record. |
| `404` | Record not found | Check that the ID or code exists. |
| `409` | Conflict | Check for a duplicate ID, duplicate email, invalid student/course reference, or duplicate enrolment. |
| `422` | Validation error | Check required fields, JSON types, age, credits, email and ID formats. |

The response code depends on the endpoint and the type of request failure. In most error responses, the `detail` field provides additional information.

## Reports, JSON exports and logging

When `python main.py` starts, it generates these reports in `reports/`:

- `You.txt` – student report
- `faculty.txt` – faculty report
- `courses.txt` – course report

It also exports current database records to `data/You.json`, `data/faculty.json`, `data/courses.json` and `data/enrollments.json`. Application log entries are written to `logs/application.log`.

## Run automated tests

Activate the virtual environment, then run the test suite from the project root:

```powershell
pytest -v
```

## Troubleshooting

**`py` or `python` is not recognised**  
Install Python and make sure the Python launcher is available on your Windows PATH. Reopen the terminal after installation.

**PowerShell blocks environment activation**  
Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current terminal, then activate `.venv` again.

**`No module named ...`**  
Make sure the virtual environment is activated and run `pip install -r requirements.txt` from the project root.

**The browser cannot connect to `127.0.0.1:8000`**  
Check that `python main.py` is still running and that the terminal has not reported an error. If the port is already in use, stop the other process using it before restarting this application.

**An enrolment request returns `Invalid student` or `Invalid course`**  
Use IDs returned by `GET /You` and `GET /courses`. The referenced records must already exist.

**An enrolment request returns a conflict**  
Check that the student is not already enrolled in that course and that the enrolment ID is not already in use.

## Project scope and limitations

CampusHub ERP is intended for learning and demonstrating backend development concepts. It is not a production-ready ERP system. The current version does not include user authentication, role-based access control, a graphical administration dashboard, deployment configuration or production-grade security controls.
