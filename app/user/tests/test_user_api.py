"""
Test for user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import APIClient
from rest_framework import status

#create as an endpoint
CREATE_USER_URL = reverse('user:create')

#add any params that we want
def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""   
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
    
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user= get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data) #makes sure there's not password in the data
        
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password':'testpass123',
            'name': 'Test Name',
        }
        #takes all arguments
        create_user(**payload)
        res= self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars. 
        make sure there is no password and make sure there is no user with that password """
        payload = {
            'email': 'test@example.com',
            'password':'pw',
            'name': 'Test Name',
        }
        res= self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)