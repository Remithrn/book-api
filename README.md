# Book Management API

## Overview

The Book Management API is a Django REST application that provides endpoints to manage books, users, and reading lists. Key features include:

- **Custom User Model:** Enforces unique username and email.
- **JWT Authentication:** Secure login and token management using JWT.
- **dj-rest-auth Integration:** Provides endpoints for login, logout, password change, password reset, and user registration.
- **Book Management:** Create, update, retrieve, and delete books.
- **Reading List Management:** Organize books in reading lists with automatic ordering and update capabilities.
- **API Documentation:** Automatically generated OpenAPI documentation using drf-spectacular.

## Features

- **User Management:**
  - Register new users.
  - Manage user profiles.
  - Unique username and email enforcement.
- **Authentication:**
  - JWT-based authentication.
  - Endpoints provided by dj-rest-auth for login, logout, and password management.
- **Book Management:**
  - CRUD operations for books.
- **Reading List Management:**
  - Create reading lists.
  - Add books to reading lists (with automatic order assignment).
  - Remove books and update their order.
- **API Documentation:**
  - Interactive documentation available through Swagger UI and ReDoc.
  - Schema generated using drf-spectacular.

## Installation

### Prerequisites

- Python 3.x
- pip

### Setup Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Remithrn/book-api.git
   cd book-api
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   # On Unix/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

install requirements:

```bash
pip install -r requirements.txt
```

4. **Apply Migrations:**

   Since a custom user model is used, run:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### User Authentication & Management

- **User Registration (dj-rest-auth):**  
  `POST /api/auth/register/`  
  _Payload Example:_

  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "yourpassword",
    "password2": "yourpassword",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

- **Login:**  
  `POST /api/auth/login/`  
  _Payload Example:_
  ```json
  {
    "username": "johndoe",
    "password": "yourpassword"
  }
  ```
- **Logout:**  
  `POST /api/auth/logout/`

- **Password Change:**  
  `POST /api/auth/password/change/`  
  _Payload Example:_

  ```json
  {
    "new_password1": "newpassword",
    "new_password2": "newpassword"
  }
  ```

- **Password Reset:**  
  `POST /api/auth/password/reset/`  
  _Payload Example:_

  ```json
  {
    "email": "john@example.com"
  }
  ```

- **Password Reset Confirm:**  
  `POST /api/auth/password/reset/confirm/`  
  _Payload Example:_

  ```json
  {
    "uid": "MQ",
    "token": "set-your-token-here",
    "new_password1": "newpassword",
    "new_password2": "newpassword"
  }
  ```

- **User Profile:**  
  `GET/PUT /api/auth/user/`  
  _Payload Example for Update:_
  ```json
  {
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

### Book Management

- **List/Create Books:**  
  `GET/POST /api/app/books/`
- **Book Detail (Retrieve/Update/Delete):**  
  `GET/PUT/PATCH/DELETE /api/app/books/{id}/`

### Reading List Management

- **List/Create Reading Lists:**  
  `GET/POST /api/app/readinglists/`

- **Reading List Detail (Retrieve/Update/Delete):**  
  `GET/PUT/PATCH/DELETE /api/app/readinglists/{id}/`

- **Add a Book to a Reading List:**  
  `POST /api/app/readinglists/{reading_list_id}/add_book/`  
  _Payload Example:_

  ```json
  {
    "book_id": 1
  }
  ```

- **Remove a Book from a Reading List:**  
  `DELETE /api/app/readinglists/{reading_list_id}/remove_book/{item_id}/`

- **Update Reading List Item Order:**  
  `PUT/PATCH /api/app/readinglists/{reading_list_id}/update_item/{id}/`  
  _Payload Example:_
  ```json
  {
    "order": 2
  }
  ```

### JWT Token Management

- **Obtain Token:**  
  `POST /api/token/`

- **Refresh Token:**  
  `POST /api/token/refresh/`

- **Verify Token:**  
  `POST /api/auth/token/verify/`

## API Documentation with drf-spectacular

Interactive API documentation is generated automatically using drf-spectacular. To use it:

1. **Configure drf-spectacular Settings:**

   In your Django settings (e.g., `settings.py`), include a configuration such as:

   ```python
   SPECTACULAR_SETTINGS = {
       'TITLE': 'Book Management API',
       'DESCRIPTION': (
           'A REST API for managing books, users, and reading lists. '
           'Provides endpoints for user registration, JWT authentication, '
           'book management, and organizing reading lists.'
       ),
       'VERSION': '1.0.0',
       'SERVE_INCLUDE_SCHEMA': False,
   }
   ```

2. **Access the API Documentation:**

   - **Swagger UI:**  
     [http://127.0.0.1:8000/api/schema/swagger-ui](http://127.0.0.1:8000/api/schema/swagger-ui)
   - **ReDoc:**  
     [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

3. **Regenerate or Export the Schema (Optional):**

   If you need to export the OpenAPI schema to a file, run:

   ```bash
   python manage.py spectacular --file schema.yaml
   ```

   This will generate a file (for example, `schema.yaml`) containing your API documentation in OpenAPI 3.0 format.

## Extensibility

- **Custom Endpoints:** Additional endpoints (such as advanced ordering or nested updates) can be added as needed.
- **dj-rest-auth:** You can further customize dj-rest-auth endpoints by overriding its serializers and views if necessary.

## Contributing

Contributions and suggestions are welcome. Please open an issue or submit a pull request with your changes.
