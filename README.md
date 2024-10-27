# JWKS-Server-SQL
Updated JWKS server that includes SQL


This is the second project in my foundations of cybersecurity class. The requirements were to have SQLite backend storage and save the private keys to a database. This project is in Python and will generate RSA key pairs, manage key expiration, ensure only the unpaired keys are available in the server, and add the new requirements. The original files, unedited, GitHub link: https://github.com/AstroPryor/JWKS_SERVER

To run this project, you need to have Python 3.anything, flask, pyjwt, requests, and Cryptography installed along with unittest and coverage, and SQLite. From there, copy the repository and create and activate a virtual machine. The server will then run on the local host 8080 and you can interact with it using curl.

The features in this code are:
- Generates RSA key pairs.
- Manages key expiration.
- Ensures only unpaired keys are available on the server.
- Tests the `/auth` endpoint for both unexpired and expired JWTs.
- Tests the JWKS endpoint for retrieving JSON Web Key Sets.
- Uses `unittest` for testing and `unittest.mock` to mock HTTP requests.

To run the code
1. Ensure that all of the packages mentioned above are installed
2. Then create and activate your virtual machine, I used venv
3. Then run the server in one terminal using python app.py
3. Then run the test script

To run the tests
1. Use python -m unittest test_jwt.py
2. Then install the coverage package
3. Then run the tests using coverage
4. Type coverage run -m unittest test_jwt.py
5. Type coverage report -m
