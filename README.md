

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
    "email": "chiemezienjoku@example.com",
    "password": "securepassword123()"
}
```

**Response Example:**
```json

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

```


#### 3. ProfileAPI

**URL:** `api/v1/auth/profile/`

**Method:** `GET`
Accessing user profile

**Request Example:**
```
GET api/v1/auth/profile/
```

```json
Headers:
Authorization: Bearer <token>
```

**Response Example:**
```json

```

**Method:** `PUT`
Updating user profile

**Request Example:**
```
PUT api/v1/auth/profile/
```

```json
Headers:
Authorization: Bearer <token>

{
    "first_name": "Chiemezie",
    "last_name": "Njoku",
    "username": "manuelinfosec",
    "email": "chiemezienjoku@example.com"
}
```

**Response Example:**
```json

```

#### 4. UserUpdatePasswordAPI

**URL:** `api/v1/auth/profile/password/`

**Method:** `POST`
Updating user password

**Request Example:**
```
POST api/v1/auth/profile/password/
```

```json
Headers:
Authorization: Bearer <token>

{
    "old_password": "securepassword123()",
    "new_password_1": "newsecurepassword123!!",
    "new_password_2": "newsecurepassword123!!"
}
```

**Response Example:**
```json

```

#### Logout (Not implemented)
- Application relies on expiration of JWT tokens for logout.

### Task Management