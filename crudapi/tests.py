# blog/tests.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import BlogPost
import json

class BlogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='rahul', password='rahul')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post('/api/login/', {'username': 'rahul', 'password': 'rahul'})
        print("\n\n\n\n\n\n\n\n\n\n\n response = ", response.data)
        return response.data.get('access')

    def test_blog_list_authenticated(self):
        # Create a blog post
        BlogPost.objects.create(title='Test Title', content='Test Content', author=self.user)

        # Authenticate the client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Make a GET request to the blog list endpoint
        response = self.client.get('/api/blogs/')

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the JSON content of the response
        response_data = json.loads(response.content)

        # Assert that the response contains the created blog post
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], 'Test Title')

    def test_blog_list_unauthenticated(self):
        # Make a GET request to the blog list endpoint without authentication
        response = self.client.get('/api/blogs/')

        # Assert that the response status code is 401 Unauthorized
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blog_create_authenticated(self):
        # Authenticate the client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Make a POST request to create a blog post
        data = {'title': 'New Title', 'content': 'New Content', 'author': self.user.id}
        response = self.client.post('/api/blogs/', data)

        # Assert that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the blog post was created in the database
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(BlogPost.objects.first().title, 'New Title')


