from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient 
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """Test the user api"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """testing create user sucessful"""
        payload = {
            'email': 'test@gmail.com',
            'password':'passtest123',
            'name': 'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """test the dupicated user"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'passtest123',
            'name': 'yoyo',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_quality(self):
        """Test that the password is more than 6 characters"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'pas',
            'name': 'yoyo',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_user_token(self):
        """Test the token is created for the user"""
        payload = {'email':'test@gmail.com','password':'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)
        
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_invalid(self):
        """If the invalid credential, not create token"""
        create_user(email='test@gmail.com',password='passtest')
        payload = {'email': 'test@gmail.com', 'password': '123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_create_token_no_user(self):
        """"If user do no exist, not create token"""
        payload={'email':'test@gmail.com','password':'passtest'}
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_field(self):
        """The email and password are required"""
        res = self.client.post(TOKEN_URL,{'email':'test','password':''})
        
        self.assertNotIn('token',res.data) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




