# api.taskmaster-django

## Project Objective
### Task 1: API Development
Develop a RESTful API for a simple task management system with the following features:
- User Authentication: Implement authentication using JWT tokens.
- CRUD Operations: Implement endpoints for creating, reading, updating, and deleting tasks.
- Data Persistence: Use a database of your choice to store task data.
- Input Validation: Validate input data to ensure data integrity and security.


### Task 2: Documentation
Document your API endpoints, data models, and any other relevant information necessary for understanding and using your code. Provide clear and concise documentation to aid future developers who may work with your code.

### Task 3: Streaming
Make sure to create a socket to stream the data created In real-time.

## Deployment
### Running the Application in Development Mode

To run this Django application in development mode, follow these steps:

1. **Clone the Repository**

    Clone the project repository to your local machine:
    ```bash
    git clone https://github.com/manuelinfosec/api.taskmaster-django.git
    cd api.taskmaster-django
    ```

2. **Create and Activate a Virtual Environment**

    It's good practice to use a virtual environment to manage dependencies:
    ```bash
    python -m venv .venv
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**

    Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**

    Apply the database migrations to set up your database schema:
    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server**

    Start the development server:
    ```bash
    python manage.py runserver
    ```

    You can now access the application at `http://127.0.0.1:8000/`.

### Deploying the Django Application to Production with Docker-Compose

To deploy the application to production using Docker-Compose, follow these steps:

1. **Clone the Repository**

    Clone the project repository to your server:
    ```bash
    git clone https://github.com/manuelinfosec/api.taskmaster-django.git
    cd api.taskmaster-django
    ```

2. **Create Environment Variables File**

    Create a `.env` file in the root directory with the following content:
    ```env
    SECRET_KEY=
    ENVIRONMENT=
    DB_USER=
    DB_PASSWORD=
    DB_NAME=
    DB_HOST=
    DB_PORT=
    ```

3. **Build and Run the Containers**

    Build the Docker images and start the containers:
    ```bash
    docker-compose up --build -d
    ```

4. **Run Migrations**

    Apply the database migrations inside the running web container:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. **Create a Superuser**

    Create a superuser for accessing the admin interface:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

6. **Access the Application**

    Your application should now be running and accessible at `http://domain.com`.

### Additional Notes
- For persistence, this project uses SQLite in development mode and PostgreSQL in a production environment.
- Ensure you have Docker and Docker-Compose installed.
- Update the `.env` file with your production environment variables.
- For SSL/TLS, consider using a reverse proxy like Nginx or Traefik to handle HTTPS connections.


## Validation and Constraints Implemented
- User Authentication:
  - Duplicate username or email is not allowed.
  - Username can only contain letters, numbers and underscore.
  - Passwords have a minimum length of 6 characters.
  - JWT access tokens have a lifetime of 7 days from last login and refresh tokens have a lifetiem for 14 days.

- Task Management
  - Task status can only be any of the following: TO DO, IN PROGRESS, DONE.

## API Documentation
### User Authentication
#### 1. Register User

**URL:** `api/v1/auth/register/`

**Method:** `POST`

Register a new user

**Request Example:**
```
POST api/v1/auth/register/
```

```json
{
    "first_name": "Chiemezie",
    "last_name": "Njoku",
    "username": "chiemezienjoku",
    "email": "njokuchiemezie01@gmail.com",
    "password": "securepassword123()"
}
```

**Response Example:**
```json
{
    "id": "ba897d82-a592-4fb5-990d-f3310f3c99dc",
    "first_name": "Chiemezie",
    "last_name": "Njoku",
    "username": "chiemezienjoku",
    "email": "njokuchiemezie01@gmail.com",
    "last_updated": "2024-05-16T04:17:48.532089+01:00",
    "last_login": "2024-05-16T04:17:48.052070+01:00",
    "is_superuser": false,
    "tokens": {
        "access": "<access_token>",
        "refresh": "<refresh_token>"
    }
}
```

#### 2. LoginAPI


**URL:** `api/v1/auth/login/`

**Method:** `POST`

Existing user login

**Request Example:**
```
POST api/v1/auth/login/
```

```json
{
    "username": "chiemezienjoku",
    "password": "securepassword123"
}
```

**Response Example:**
```json
{
    "id": "ba897d82-a592-4fb5-990d-f3310f3c99dc",
    "first_name": "Chiemezie",
    "last_name": "Njoku",
    "username": "chiemezienjoku",
    "email": "njokuchiemezie01@gmail.com",
    "last_updated": "2024-05-16T04:17:48.532089+01:00",
    "last_login": "2024-05-16T04:17:48.052070+01:00",
    "is_superuser": false,
    "tokens": {
        "access": "<access_token>",
        "refresh": "<refresh_token>"
    }
}
```

#### 3.  Logout (Not implemented)
- Application relies on expiration of JWT tokens for logout.

#### 4. ProfileAPI

**URL:** `api/v1/auth/profile/`

**Method:** `GET`

Accessing user profile

**Request Example:**
```
GET api/v1/auth/profile/

Headers:
Authorization: Bearer <access_token>
```

**Response Example:**
```json
{
    "id": "ba897d82-a592-4fb5-990d-f3310f3c99dc",
    "first_name": "Chiemezie",
    "last_name": "Njoku",
    "username": "chiemezienjoku",
    "email": "njokuchiemezie01@gmail.com",
    "last_updated": "2024-05-16T04:24:53.688303+01:00",
    "last_login": "2024-05-16T04:24:53.688303+01:00",
    "is_superuser": false
}
```

**Method:** `PATCH`

Updating user profile

**Request Example:**
```
PATCH api/v1/auth/profile/

Headers:
Authorization: Bearer <access_token>
```

```json

{
    "username": "manuelinfosec",
}
```

**Response Example:**
```json
{
    "id": "ba897d82-a592-4fb5-990d-f3310f3c99dc",
    "first_name": "Chiemezie",
    "last_name": "Njoku",
    "username": "manuelinfosec",
    "email": "chiemezienjoku@example.com",
    "last_updated": "2024-05-16T04:29:16.296174+01:00",
    "last_login": "2024-05-16T04:24:53.688303+01:00",
    "is_superuser": false
}
```

#### 5. UserUpdatePasswordAPI

**URL:** `api/v1/auth/profile/password/`

**Method:** `POST`

Updating user password

**Request Example:**
```
POST api/v1/auth/profile/password/

Headers:
Authorization: Bearer <access_token>
```

```json
{
    "old_password": "securepassword123()",
    "new_password_1": "newsecurepassword123!!",
    "new_password_2": "newsecurepassword123!!"
}
```

**Response Example:**
```json
{
    "detail": "password updated successfully"
}
```

#### 6. TokenVerify
**URL:** `api/v1/auth/token/verify/`

**Method:** `POST`

Verifying a user token

Request Example:

```
POST api/v1/auth/token/verify/

Headers:
Content-Type: application/json
```

**Request Example:**
```json
{
    "token": "<access_token>"
}
```

**Response Example:**
```json
{
    "message": "Token is valid"
}
```

#### 6. TokenRefresh
**URL:** `api/v1/auth/token/refresh/`

**Method:** `POST`

Refreshing a user token

Request Example:
```
POST api/v1/auth/token/refresh/

Headers:
Content-Type: application/json
```

**Request Example::**
```json
{
    "refresh": "<refresh_token>"
}

```
**Response Example:**
```json
{
    "access": "<new_access_token>",
    "refresh": "<new_refresh_token>"
}

```

### Task Management

#### 1. Create Task
**URL:** `api/v1/tasks/`

**Method:** `POST`

Creating a new task

**Request Example:**
```
POST api/v1/tasks/

Headers:
Content-Type: application/json
Authorization: Bearer <access_token>
```

```json
{
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "TO DO"
}
```

**Response Example:**
```json
{
    "id": "4870ffda-363c-4795-a15b-136d171f14c3",
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "TO DO",
    "date_created": "2024-05-16T22:08:05.319718+01:00",
    "last_updated": "2024-05-16T22:08:05.319718+01:00"
}
```


#### 2. GetTask

**URL:** `api/v1/tasks/{task_id}/`

**Method:** `GET`

Retrieving a single task by ID

**Request Example:**
```
GET api/v1/tasks/4870ffda-363c-4795-a15b-136d171f14c3/

Headers:
Authorization: Bearer <access_token>
```

**Response Example:**
```json
{
    "id": "4870ffda-363c-4795-a15b-136d171f14c3",
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "TO DO",
    "date_created": "2024-05-16T22:08:05.319718+01:00",
    "last_updated": "2024-05-16T22:08:05.319718+01:00"
}
```

#### 3. Update Task

**URL:** `api/v1/tasks/{task_id}/`

**Method:** `PUT`

Updating a single task by ID

**Request Example:**
```
PUT api/v1/tasks/4870ffda-363c-4795-a15b-136d171f14c3/

Headers:
Content-Type: application/json
Authorization: Bearer <access_token>
```

```json
{
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "DONE"
}
```

**Response Example:**

```json
{
    "id": "4870ffda-363c-4795-a15b-136d171f14c3",
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "DONE",
    "date_created": "2024-05-16T22:08:05.319718+01:00",
    "last_updated": "2024-05-16T22:11:10.519238+01:00"
}
```


#### 4. Delete Task

**URL:** `api/v1/tasks/{task_id}/`

**Method:** `DELETE`

Deleting a single task by ID

**Request Example:**

```
DELETE api/v1/tasks/4870ffda-363c-4795-a15b-136d171f14c3/

Headers:
Authorization: Bearer <access_token>
```

```json
{
    "message": "Task deleted successfully"
}
```

**Response Example:**
```json
```

#### 5. List Tasks
**URL:** `api/v1/tasks/`

**Method:** `GET`

Listing all tasks

**Request Example:**

```
GET api/v1/tasks/

Headers:
Authorization: Bearer <access_token>
```

**Response Example:**
```json
{
    "count": 1,
    "previous": null,
    "next": null,
    "results": [
        {
            "id": "4870ffda-363c-4795-a15b-136d171f14c3",
            "title": "Complete Backend Assessment",
            "description": "Write and submit the project proposal",
            "status_task": "TO DO",
            "date_created": "2024-05-16T22:16:57.227019+01:00",
            "last_updated": "2024-05-16T22:16:57.227019+01:00"
        }
    ]
}
```

### Websocket Streams

Every websocket connect request is required to have the authorization token in its headers

```
Headers:
authorization: <access_token>
```

#### 1. TaskCreate Stream

**Stream URL:** `ws/tasks/`

Real-time notifications when a new task is created.

***Response Example:**
```json
{
    "id": "4870ffda-363c-4795-a15b-136d171f14c3",
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "TO DO",
    "date_created": "2024-05-17T01:40:11.499810+01:00",
    "last_updated": "2024-05-17T01:40:11.499810+01:00",
    "action": "task_create"
}
```

#### 2. TaskUpdate Stream

**Stream URL:** `ws/tasks/`

Real-time notifications when a new task is updated.

***Response Example:**
```json
{
    "id": "4870ffda-363c-4795-a15b-136d171f14c3",
    "title": "Complete Backend Assessment",
    "description": "Write and submit the project proposal",
    "status_task": "TO DO",
    "date_created": "2024-05-17T01:40:11.499810+01:00",
    "last_updated": "2024-05-17T01:40:11.499810+01:00",
    "action": "task_update"
}
```

#### 3. TaskDelete Stream

**Stream URL:** `ws/tasks/`

Real-time notifications when a new task is deleted.

***Response Example:**
```json
{
    "id": "4870ffda-363c-4795-a15b-136d171f14c3",
    "action": "task_delete"
}
```

## Testing
### Testing with Postman
For the API endpoints, a Postman collection is available in the [`postman`](/postman/) directory of this project. This collection includes all the necessary endpoints for testing user registration, authentication, and task management.

#### WebSocket Request Setup in Postman
Open Postman and go to the WebSocket tab.
Enter the WebSocket URL:
```
ws://<server-address>/ws/tasks/
```
Connect to the WebSocket by clicking the "Connect" button. Below is a screen example:

![Postman WebSocket Screenshot](/postman/image.png)


### Testing with Pytest

### Testing with Postman
For the API endpoints, a Postman collection is available in the [`postman`](/postman/) directory of this project. This collection includes all the necessary endpoints for testing user registration, authentication, and task management.

### Testing with Pytest
To ensure the proper functionality of the application, we use `pytest` for running our test suite located in the [`tests`](/tests/) directory. Follow the instructions below to set up and run the tests:

1. **Install Dependencies**:
   Make sure you have all dependencies installed by running:
   ```sh
   pip install -r requirements.txt
   ```

2. **Run the Tests**:
   Execute the following command to run the tests:
   ```sh
   pytest
   ```
   This will discover and run all the tests in the project. 

3. **Generate Coverage Report**:
   To measure test coverage, run `pytest` with the coverage option:
   ```sh
   pytest --cov=taskmanager --cov=accounts
   ```
   This command will generate a coverage report indicating how much of your code is covered by tests.

4. **View Detailed Coverage Report**:
   To generate a detailed HTML report of the test coverage, use:
   ```sh
   pytest --cov=taskmanager --cov=accounts --cov-report=html
   ```
   The report will be available in the `htmlcov` directory. Open the `index.html` file in your browser to view the detailed report.

## Issues Encountered

### 1. WebSocket Notifications Not Scoped to the Correct User
**Description:**
WebSocket notifications are currently not scoped to the correct user. Task notifications are broadcast to all users subscribed to the WebSocket channel, resulting in users receiving irrelevant task updates that are not associated with them.

**Fix:**
To resolve this issue, the WebSocket implementation was modified to ensure that notifications are only sent to the specific user associated with the task. This was achieved by creating unique WebSocket groups for each user based on the `user_id` and sending notifications to the appropriate group.
