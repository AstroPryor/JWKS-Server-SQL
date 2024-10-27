import requests
import unittest
from unittest.mock import patch

def test_auth_endpoint(expired=False):
    url = 'http://localhost:8080/auth'
    if expired:
        url += '?expired=true'
    response = requests.post(url)
    return response.json()

def test_jwks_endpoint():
    response = requests.get('http://localhost:8080/.well-known/jwks.json')
    return response.json()

class TestEndpoints(unittest.TestCase):

    @patch('requests.post')
    def test_auth_endpoint_unexpired(self, mock_post):
        # Arrange
        mock_post.return_value.json.return_value = {'token': 'valid_jwt'}
        
        # Act
        result = test_auth_endpoint()
        
        # Assert
        self.assertEqual(result, {'token': 'valid_jwt'})
        mock_post.assert_called_once_with('http://localhost:8080/auth')

    @patch('requests.post')
    def test_auth_endpoint_expired(self, mock_post):
        # Arrange
        mock_post.return_value.json.return_value = {'error': 'token expired'}
        
        # Act
        result = test_auth_endpoint(expired=True)
        
        # Assert
        self.assertEqual(result, {'error': 'token expired'})
        mock_post.assert_called_once_with('http://localhost:8080/auth?expired=true')

    @patch('requests.get')
    def test_jwks_endpoint(self, mock_get):
        # Arrange
        mock_get.return_value.json.return_value = {'keys': ['key1', 'key2']}
        
        # Act
        result = test_jwks_endpoint()
        
        # Assert
        self.assertEqual(result, {'keys': ['key1', 'key2']})
        mock_get.assert_called_once_with('http://localhost:8080/.well-known/jwks.json')

if __name__ == '__main__':
    unittest.main()
