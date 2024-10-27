import sqlite3
import jwt
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

DATABASE = 'totally_not_my_privateKeys.db'

# Utility to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the keys table if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            key BLOB NOT NULL,
            exp INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Generate a new RSA key pair and store it in the database
def generate_and_store_key(expiry_duration):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Serialize the private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    expiry_time = int((datetime.utcnow() + expiry_duration).timestamp())

    # Store the key in the database
    conn = get_db_connection()
    conn.execute('INSERT INTO keys (key, exp) VALUES (?, ?)', (private_key_pem, expiry_time))
    conn.commit()
    conn.close()

# Fetch the private key from the database
def get_key(expired=False):
    conn = get_db_connection()
    if expired:
        result = conn.execute('SELECT key FROM keys WHERE exp < ?', (int(datetime.utcnow().timestamp()),)).fetchone()
    else:
        result = conn.execute('SELECT key FROM keys WHERE exp > ?', (int(datetime.utcnow().timestamp()),)).fetchone()
    conn.close()
    
    if result:
        return serialization.load_pem_private_key(result['key'], password=None, backend=default_backend())
    return None

# Fetch all valid keys for the JWKS endpoint
def get_valid_keys():
    conn = get_db_connection()
    keys = conn.execute('SELECT key FROM keys WHERE exp > ?', (int(datetime.utcnow().timestamp()),)).fetchall()
    conn.close()
    
    public_keys = []
    for row in keys:
        private_key = serialization.load_pem_private_key(row['key'], password=None, backend=default_backend())
        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_keys.append(public_key_pem)
    
    return public_keys

# JWKS Endpoint
@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    valid_keys = get_valid_keys()
    jwks_data = {'keys': []}

    for public_key_pem in valid_keys:
        jwks_data['keys'].append({
            'kid': '1',  # Simplified, you should generate a unique KID
            'kty': 'RSA',
            'use': 'sig',
            'alg': 'RS256',
            'n': '',  # You should encode the 'n' and 'e' from the public key properly here
            'e': ''
        })
    return jsonify(jwks_data)

# Authentication Endpoint
@app.route('/auth', methods=['POST'])
def auth():
    expired = 'expired' in request.args
    private_key = get_key(expired)

    if private_key is None:
        return jsonify({'error': 'No valid key found'}), 400

    payload = {'username': 'userABC', 'exp': datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': '1'})
    
    return jsonify({'token': token})

if __name__ == '__main__':
    create_table()
    # Generate one key that expires now and one that expires in an hour
    generate_and_store_key(timedelta(seconds=-10))  # Expired key
    generate_and_store_key(timedelta(hours=1))  # Valid key
    app.run(port=8080)
