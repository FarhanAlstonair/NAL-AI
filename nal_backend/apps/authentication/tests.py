import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'role': 'BUYER'
        }

    def test_user_registration(self):
        """Test user registration"""
        url = reverse('auth-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        url = reverse('auth-login')
        response = self.client.post(url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'invalid@example.com',
            'password': 'wrongpass'
        }
        
        url = reverse('auth-login')
        response = self.client.post(url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])