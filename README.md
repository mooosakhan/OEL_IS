

# Flask User Authentication API with MySQL

This is a simple Flask application that provides a user authentication system with **signup** and **login** functionalities, including **password hashing** for security. The app uses **MySQL** as the database to store user information and supports secure password storage using the **PBKDF2 hashing algorithm**.

## Features

- **User Signup**: Allows users to register by providing a username and password. The password is securely hashed before storing in the database.
- **User Login**: Authenticates users by checking their username and password. The entered password is verified against the stored hash.
- **Password Hashing**: Passwords are securely hashed using the **PBKDF2** method, ensuring sensitive information is protected.
- **MySQL Integration**: The app connects to a MySQL database to store and retrieve user information.

## Prerequisites

Before running this app, you need to have the following installed:

- **Python 3.x**
- **MySQL Server** (or a running MySQL service)
- **pip** (Python package manager)

You also need to have a MySQL database with a `users` table to store the user data.

### Required Python Packages

To install the required Python packages, you can use `pip`:

```bash
pip install Flask mysql-connector-python werkzeug
```

## Setting Up the MySQL Database

1. Create a database in MySQL (replace `usersdb` with your preferred name):

```sql
CREATE DATABASE usersdb;
```

2. Create the `users` table with the following structure:

```sql
USE usersdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

This table will store the `username` and the securely hashed `password` for each user.

## Running the App

1. Clone this repository or copy the code into a Python file (e.g., `app.py`).
2. Replace the following values in the script with your own MySQL connection details:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'  # MySQL username
MYSQL_PASSWORD = 'your_password'  # Your MySQL password
MYSQL_DATABASE = 'usersdb'  # The database name
```

3. Run the Flask app:

```bash
python app.py
```

The app will start running on `http://localhost:5000`.

## API Endpoints

### 1. **User Signup**

- **URL**: `/signup`
- **Method**: `POST`
- **Body**: JSON object containing the username and password.
  
**Example Request:**
```json
{
  "username": "user123",
  "password": "mypassword"
}
```

**Response**:
- **Success (201)**: 
  ```json
  {
    "message": "User registered successfully"
  }
  ```
- **Error (400)** if username or password is missing:
  ```json
  {
    "error": "Username and password are required"
  }
  ```
- **Error (409)** if username already exists:
  ```json
  {
    "error": "Username already exists"
  }
  ```

### 2. **User Login**

- **URL**: `/login`
- **Method**: `POST`
- **Body**: JSON object containing the username and password.

**Example Request:**
```json
{
  "username": "user123",
  "password": "mypassword"
}
```

**Response**:
- **Success (200)**: 
  ```json
  {
    "message": "Login successful"
  }
  ```
- **Error (400)** if username or password is missing:
  ```json
  {
    "error": "Username and password are required"
  }
  ```
- **Error (401)** if invalid username or password:
  ```json
  {
    "error": "Invalid username or password"
  }
  ```

## Security Considerations

- **Password Hashing**: Passwords are hashed using **PBKDF2 with SHA-256** to ensure that raw passwords are never stored in the database.
- **MySQL Connection**: Make sure to secure your database credentials, especially in production environments. Use environment variables or a configuration file for better security practices.

## Error Handling

The app includes basic error handling for common scenarios:
- **Database connection errors** (e.g., if MySQL is down or credentials are incorrect).
- **Input validation errors** (e.g., missing fields in the request body).
- **Integrity errors** (e.g., duplicate usernames during signup).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

