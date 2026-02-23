#Notification API Project

## Project Description
 This project implements a notification system using Django and Django REST Framework.

## Project Setup
1. Create pfoject folder
2. Create virtual environment and activate 
3. Install dependencies:
    pip install -r requirements.txt
4. Run migrations:
    python manage.py makemigrations
    python manage.py migrate
5. Create Superuser:
    python manage.py createsuperuser
6. Run server:
    python manage.py runserver
    
- The Server will rub at:http://127.0.0.1:8000/

## Authentication
User must be authenticated to access protected endpoints.

## APIs:
- GET /notifications/ ->To get user notifications
- PATCH /notifications/{id}/read/ ->To mark notification as read

## Technologies Used
- Python
- Django
- Django Rest Framework
- SQLite

# Author
Jahnavi K
