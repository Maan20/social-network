# Social Network API

This project is a social network API built with Django, Django REST framework (DRF), and JWT for authentication. The backend uses PostgreSQL for data storage and includes endpoints for user registration, login, searching users, sending friend requests, and listing friends.

## Features

- User Registration and Login with JWT Authentication
- User Search by Username or Email
- Friend Request Management (send, accept, and reject requests)
- Friends List and Pending Requests
- Dockerized for easy setup

## Project Structure

The project consists of two apps:
1. `accounts`: Contains user and friend request models.
2. `api`: Contains views, serializers, and URLs for the API endpoints.

## Setup Instructions

### Prerequisites

Ensure you have the following installed:
- Python 3.9+
- PostgreSQL
- Docker (optional, for containerized setup)

### Clone the Repository

```bash
git clone https://github.com/Maan20/social-network.git
cd social-network
```
### .env file for credentials
```bash

    DEBUG=True
    SECRET_KEY=your_secret_key
    DB_NAME=social_network
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=db
    DB_PORT=5432

```

###  Install Dependencies
```bash
pip install -r requirements.txt
```

###  Install Dependencies
```bash
python manage.py makemigrations
python manage.py migrate
```

###  Create a Superuser
```bash
python manage.py createsuperuser
```
###  Run the Development Server

```bash
python manage.py runserver
```
* #### Run It
    Fire up the server using this one simple command:
    ```bash
         python manage.py runserver
    ```
    You can now access the file api service on your browser by using
    Access the Application
    The application will be available at 
    ```bash
    http://localhost:8000.
    ```

    API Endpoints
    # 1. User Registration
    URL: 
    ```bash
    http://localhost:8000/api/signup
    ```
        Method: POST
        Body:
        json
    ```bash
        {
            "email": "john@example.com",
            "password": "password123",
            "full_name": "John Doe",
        }
    ```
    ## 2. User Login
    URL: http://localhost:8000/api/login
    #### Method: POST
    Body:
    json
    ```bash
        {
            "email": "john@example.com",
            "password": "password123"
        }
    ```
    Recieved jwt access token in login API will be used in other API as authentication.
    # 3. User Search
    ```bash
        URL: http://localhost:8000/api/search-user
    ```
    #### Method: GET
    #### Query Parameters: ?query=<search_term> 
    ## 4. Send Friend Request
    ```bash
        URL: http://localhost:8000/api/friend-request
    ```
    Method: POST

    Body:
    json
    ```bash
        {
            "to_user_id": <user_id>
        }
    ```
    ## 5. Friends List
    URL: /api/friends

    Method: GET

    Pending Friend Requests
    ```bash
    URL: http://localhost:8000/api/pending-requests
    ```
    Method: GET

   # Check Postman collection for all API's

##  Docker Setup
###  docker-compose up --build

```bash
Build and Run Docker Containers
```

### Apply Migrations in Docker

```bash
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate
```
### Create a Superuser in Docker
```bash
docker-compose exec web python manage.py createsuperuser
```

### Create a Superuser in Docker
```bash
docker-compose exec web python manage.py createsuperuser
```


