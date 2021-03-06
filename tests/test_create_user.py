import json
import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from .test_base import TestBase,new_user,new_user_response,token_signature_error,token_expired,token_Invalid,token_header,login_user,all_users_response,invalid_login_user,login_user_response,new_user_error_mail
from api.helpers.auth import encode_token


class TestUser(TestBase):
    def test_create_user(self):
        response = self.app.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(new_user))
        self.assertEqual(response.status_code,201)
        data = response.data.decode()
        self.assertEqual(json.loads(data), new_user_response)

    def test_sign_up_with_used_mail(self):
        response = self.app.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(new_user_error_mail))
        self.assertEqual(response.status_code,406)
        data = response.data.decode()
        Invalid={"message": "sorry, Email already in use"}
        self.assertEqual(json.loads(data), Invalid)

    def test_login(self):
        response = self.app.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(login_user))
        self.assertEqual(response.status_code,200)
        data = response.data.decode()
        self.assertTrue(json.loads(data), login_user_response)

    def test_login_invalid(self):
        response = self.app.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(invalid_login_user))
        self.assertEqual(response.status_code,401)
        data = response.data.decode()
        Invalid={"message": "Invalid credentials, Please try again"}
        self.assertEqual(json.loads(data), Invalid)

    def test_get_users(self):
        response = self.app.get('/api/v1/users',headers=token_header(encode_token(1)))
        self.assertEqual(response.status_code,200)
        data = response.data.decode()
        self.assertEqual(json.loads(data)["users"][0]["email"], all_users_response["users"][0]["email"])
        self.assertEqual(json.loads(data)["users"][0]["userName"], all_users_response["users"][0]["userName"])
        self.assertEqual(json.loads(data)["users"][0]["phoneNumber"], all_users_response["users"][0]["phoneNumber"])


    def test_get_token_miss(self):
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code,401)
        data = response.data.decode()
        message={"message": "Missing token"}
        self.assertEqual(json.loads(data), message)

    def test_get_expire_token(self):
        response = self.app.get('/api/v1/users',headers=token_expired)
        self.assertEqual(response.status_code,401)
        data = response.data.decode()
        token_expired_message={"message": "token expired"}
        self.assertEqual(json.loads(data), token_expired_message)

    def test_get_invalid_token(self):
        response = self.app.get('/api/v1/users',headers=token_Invalid)
        self.assertEqual(response.status_code,401)
        data = response.data.decode()
        token_Invalid_message={"message": "Invalid Token verification failed"}
        self.assertEqual(json.loads(data), token_Invalid_message)

    def test_get_token_signature_error(self):
        response = self.app.get('/api/v1/users',headers=token_signature_error)
        self.assertEqual(response.status_code,401)
        data = response.data.decode()
        message={"message": "Signature verification failed"}
        self.assertEqual(json.loads(data), message)


    def test_some_get_users_error(self):
        response = self.app.get('/api/v1/users',headers=token_header(encode_token(2)))
        self.assertEqual(response.status_code,401)
        data = response.data.decode()
        message={"messsage": "Only admin can access this route"}
        self.assertEqual(json.loads(data), message)

if __name__ == '__main__':
    unittest.main()