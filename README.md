

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


#### 3. ProfileAPI

**URL:** `api/v1/auth/profile/`

**Method:** `GET`

Accessing user profile

**Request Example:**
```
GET api/v1/auth/profile/

Headers:
Authorization: Bearer <token>
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
Authorization: Bearer <token>
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

#### 4. UserUpdatePasswordAPI

**URL:** `api/v1/auth/profile/password/`

**Method:** `POST`

Updating user password

**Request Example:**
```
POST api/v1/auth/profile/password/

Headers:
Authorization: Bearer <token>
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

#### Logout (Not implemented)
- Application relies on expiration of JWT tokens for logout.

### Task Management