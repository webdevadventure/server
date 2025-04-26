from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_mgmt.models import User
from .models import BlogPost, Comment, Category

class BlogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        self.normal_user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        
        self.category = Category.objects.create(name='Test Category')
        
        self.blog_post = BlogPost.objects.create(
            author=self.admin_user,
            title='Test Blog Post',
            content='Test content',
            category=self.category
        )
        
        self.comment = Comment.objects.create(
            user=self.normal_user,
            target_type='blog',
            target_id=self.blog_post.id,
            content='Test comment'
        )
        
    def test_get_blog_posts(self):
        url = reverse('blogpost-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_blog_post_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('blogpost-list')
        data = {
            'title': 'New Blog Post',
            'content': 'New content',
            'category': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_blog_post_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('blogpost-list')
        data = {
            'title': 'New Blog Post',
            'content': 'New content',
            'category': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
