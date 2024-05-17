## Project Structure

This project is organized to ensure a clean and maintainable codebase. The project uses both ASGI and WSGI applications to handle different parts of the application.

### ASGI and WSGI Applications

- **ASGI Application:** Used to handle the WebSocket part of the application, enabling real-time features such as task notifications.

- **WSGI Application:** Used to handle the traditional HTTP requests for the CRUD endpoints and other standard web functionalities.


### Components

The project architecture follows a View-Service-Serializer-Model (VSSM) approach, promoting a separation of concerns and enhancing the maintainability and testability. Here's a brief explanation of each component:

1. **View**
    - Responsible for handling HTTP requests and returning HTTP responses.
    - Inherits from Django’s `View` classes (e.g., `APIView`, `ViewSet`).

2. **Service**
    - Contains the business logic of the application.
    - Decouples the business logic from the views, making it easier to test and maintain.

3. **Serializer**
    - Translates complex data types (e.g., querysets) into JSON and vice versa.
    - Validates incoming data to ensure it meets the expected format.

4. **Model**
    - Defines the structure of the data in the application.
    - Represents the database schema using Django’s ORM (Object-Relational Mapping).



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

**Method:** `PUT`

Updating user profile

**Request Example:**
```
PUT api/v1/auth/profile/

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


Sure, here are the request examples for the Task views:

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
    "last_updated": "2024-05-17T01:40:11.499810+01:00"
}
```


## Testing with Postman
For the API endpoints, a Postman collection is available in the [`postman`](/postman/) directory of this project. This collection includes all the necessary endpoints for testing user registration, authentication, and task management.

### WebSocket Request Setup in Postman
Open Postman and go to the WebSocket tab.
Enter the WebSocket URL:
```
ws://<server-address>/ws/tasks/
```
Connect to the WebSocket by clicking the "Connect" button. Below is a screen example:

![Postman WebSocket Screenshot](/postman/image.png)
