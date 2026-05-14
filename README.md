# JWKS Server with SQLite Storage

## Overview

This project was developed for my Foundations of Cybersecurity course at the University of North Texas. It is the second version of my RESTful JSON Web Key Set (JWKS) server project.

This version builds on the original JWKS server by adding SQLite-backed storage for RSA private keys. Instead of only managing keys in memory, this version stores key data in a local database and retrieves valid keys when needed.

The server generates RSA key pairs, manages key expiration, signs JSON Web Tokens, and serves valid public keys through a JWKS endpoint.

Original base version:

```text
https://github.com/AstroPryor/JWKS_SERVER
```

## Purpose

The purpose of this project was to:

- Extend the original JWKS server with SQLite database storage
- Store private keys in a database
- Generate RSA public/private key pairs
- Create signed JSON Web Tokens
- Serve valid public keys through a JWKS endpoint
- Handle expired keys correctly
- Test both valid and expired JWT behavior
- Practice backend security concepts using Python, Flask, JWTs, RSA keys, and SQLite

## Technologies Used

- Python
- Flask
- PyJWT
- Cryptography
- SQLite
- unittest
- unittest.mock
- coverage
- requests

## Repository Structure

```text
JWKS-Server-SQL/
├── Gradebot P2.png
├── P2 test_suite.png
├── README.md
├── Test Output SQL.png
├── app.py
└── test_app.py
```

## File Descriptions

### `app.py`

`app.py` is the main Flask application for the SQLite-backed JWKS server. It contains the application logic for generating RSA keys, storing private keys in SQLite, creating JWTs, serving public keys, and managing key expiration.

This file is responsible for:

- Starting the Flask server
- Creating or connecting to the SQLite database
- Generating RSA public/private key pairs
- Storing private keys in the database
- Retrieving valid keys from the database
- Creating signed JSON Web Tokens
- Returning public keys in JWKS format
- Managing key expiration
- Handling the `/auth` endpoint
- Handling the `/.well-known/jwks.json` endpoint

### `test_app.py`

`test_app.py` contains the unit tests for this version of the project. The tests verify that the SQLite-backed JWKS server works correctly and that the required endpoints behave as expected.

This file is responsible for testing:

- JWKS endpoint responses
- Authentication endpoint responses
- JWT generation
- Expired JWT behavior
- Database-backed key retrieval
- Key expiration handling
- Basic server functionality
- Mocked HTTP request behavior where needed

### `Gradebot P2.png`

`Gradebot P2.png` is a screenshot related to the project grading or submission results.

### `P2 test_suite.png`

`P2 test_suite.png` is a screenshot showing test suite results for the project.

### `Test Output SQL.png`

`Test Output SQL.png` is a screenshot showing test or coverage output for the SQLite version of the JWKS server.

## Features

This project includes the following features:

- Generates RSA public/private key pairs
- Stores private keys in a SQLite database
- Manages key expiration
- Ensures only valid, non-expired public keys are available through the JWKS endpoint
- Creates signed JWTs through the authentication endpoint
- Tests the `/auth` endpoint for valid and expired JWT behavior
- Tests the JWKS endpoint for retrieving JSON Web Key Sets
- Uses `unittest` for automated testing
- Uses `unittest.mock` to mock HTTP requests where needed
- Uses `coverage` to measure test coverage

## Endpoints

### JWKS Endpoint

```http
GET /.well-known/jwks.json
```

This endpoint returns the currently available public keys in JWKS format. These public keys can be used by clients to verify JWTs signed by the server.

Example request:

```bash
curl http://127.0.0.1:8080/.well-known/jwks.json
```

Expected behavior:

- Returns a JSON Web Key Set
- Includes valid, non-expired public keys
- Does not expose private keys
- Retrieves key information from the SQLite-backed key storage logic

### Authentication Endpoint

```http
POST /auth
```

This endpoint returns a signed JWT using one of the available RSA private keys.

Example request:

```bash
curl -X POST http://127.0.0.1:8080/auth
```

Expected behavior:

- Generates a signed JWT
- Uses an available RSA private key
- Returns the token to the client
- Supports testing of valid and expired JWT behavior

## How to Run

### 1. Install Python

Make sure Python 3.x is installed.

Check your Python version with:

```bash
python --version
```

or:

```bash
python3 --version
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

Replace `<repository-url>` with the actual GitHub repository URL.

Replace `<repository-name>` with the folder name created after cloning the repository.

### 3. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install the required Python packages:

```bash
pip install flask pyjwt cryptography requests coverage
```

SQLite is included with Python through the built-in `sqlite3` module, so a separate SQLite Python package is usually not required.

If a `requirements.txt` file is added later, dependencies can be installed with:

```bash
pip install -r requirements.txt
```

### 5. Run the Server

```bash
python app.py
```

The server runs locally at:

```text
http://127.0.0.1:8080
```

## Testing the Server Manually

### Test the JWKS Endpoint

Run:

```bash
curl http://127.0.0.1:8080/.well-known/jwks.json
```

This should return the available public keys in JWKS format.

### Test the Authentication Endpoint

Run:

```bash
curl -X POST http://127.0.0.1:8080/auth
```

This should return a signed JWT.

## Running Unit Tests

Run the unit tests with:

```bash
python -m unittest test_app.py
```

This command runs the test cases in `test_app.py` and verifies that the main parts of the server are functioning correctly.

## Running Tests with Coverage

To run the tests with coverage tracking:

```bash
coverage run -m unittest test_app.py
coverage report -m
```

This shows how much of the project code is covered by the unit tests and displays missing lines if coverage is incomplete.

## Test Output

The repository includes screenshots showing the test and grading output for this project:

```text
Gradebot P2.png
P2 test_suite.png
Test Output SQL.png
```

If the images do not display correctly on GitHub because of spaces in the file names, rename them to:

```text
gradebot-p2.png
p2-test-suite.png
test-output-sql.png
```

Then update the image links to:

```markdown
![Gradebot P2 Output](gradebot-p2.png)
![P2 Test Suite Output](p2-test-suite.png)
![SQL Test Output](test-output-sql.png)
```

Current image links:

```markdown
![Gradebot P2 Output](Gradebot%20P2.png)
![P2 Test Suite Output](P2%20test_suite.png)
![SQL Test Output](Test%20Output%20SQL.png)
```

![Gradebot P2 Output](Gradebot%20P2.png)

![P2 Test Suite Output](P2%20test_suite.png)

![SQL Test Output](Test%20Output%20SQL.png)

## What I Learned

Through this project, I gained hands-on experience with:

- Extending an existing security-focused backend project
- Using SQLite for local database storage
- Storing and retrieving private key data
- Generating RSA public/private key pairs
- Creating and signing JSON Web Tokens
- Understanding JSON Web Key Sets
- Managing key expiration
- Testing valid and expired JWT behavior
- Writing Python unit tests
- Using `unittest.mock` for testing
- Measuring test coverage
- Connecting backend security concepts with persistent storage

This project helped me better understand how authentication systems can store key material, retrieve valid keys, expose public keys for JWT verification, and manage expired keys securely.

## Related Versions

This repository is the second version of the JWKS server project.

Related versions include:

- Base RESTful JWKS server with in-memory key handling
- SQLite-backed JWKS server
- AES-encrypted private key storage version
- Version with user registration, authentication logging, and rate limiting

This version specifically focuses on adding database-backed storage to the original JWKS server.

## Disclaimer

This project was created for educational purposes as part of a cybersecurity course. It is intended to demonstrate JWKS, JWT, RSA key handling, SQLite-backed key storage, key expiration, and basic REST API security concepts in a controlled local environment.

This project is not intended for production use without additional security hardening, encrypted key storage, access control, configuration management, and secure deployment practices.
