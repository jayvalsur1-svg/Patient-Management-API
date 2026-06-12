# Patient Management REST API

A RESTful API built with FastAPI for managing patient records. This project demonstrates backend development concepts such as CRUD operations, request validation, computed fields, query parameters, path parameters, and error handling.

## Features

* Create patient records
* View all patients
* Retrieve patient by ID
* Update patient information
* Delete patient records
* Sort patients by BMI, height, or weight
* Automatic BMI calculation
* Automatic health verdict generation
* Input validation using Pydantic
* Interactive API documentation

## Technologies Used

* Python
* FastAPI
* Pydantic V2
* JSON
* REST API

## Project Structure

```text
.
├── main.py
├── data.json
└── README.md
```

## Patient Data Model

```json
{
  "id": "P001",
  "name": "Luffy",
  "city": "Wano",
  "age": 19,
  "gender": "Male",
  "height": 1.74,
  "weight": 64
}
```

## Computed Fields

The API automatically calculates:

### BMI

```text
BMI = Weight / (Height²)
```

### Health Verdict

| BMI Range  | Verdict     |
| ---------- | ----------- |
| < 18       | Underweight |
| 18 - 24.99 | Normal      |
| 25 - 29.99 | Overweight  |
| >= 30      | Obese       |

## API Endpoints

### Home

```http
GET /
```

### About

```http
GET /about
```

### View All Patients

```http
GET /view
```

### Get Patient By ID

```http
GET /patient/{patient_id}
```

### Create Patient

```http
POST /create
```

### Update Patient

```http
PUT /update/{patient_id}
```

### Delete Patient

```http
DELETE /delete/{patient_id}
```

### Sort Patients

```http
GET /sort?sort_by=bmi&Order=desc
```

Supported sorting fields:

* bmi
* height
* weight

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd patient-management-api
```

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Run the server:

```bash
uvicorn main:app --reload
```

## API Documentation

After starting the server:

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Concepts Demonstrated

* REST API Development
* FastAPI Framework
* Pydantic Validation
* CRUD Operations
* Computed Fields
* Query Parameters
* Path Parameters
* Error Handling
* JSON Data Persistence

## Future Improvements

* SQLite or PostgreSQL Integration
* Authentication and Authorization
* Pagination
* Search Functionality
* Docker Support
* Unit Testing
* Logging System
* Deployment to Cloud Platforms

## Author

Jay Valsur

Python Developer | Backend Development Enthusiast | FastAPI Learner
