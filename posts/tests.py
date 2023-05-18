import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

import django

django.setup()
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import News, Category, Comment
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class TestGetAllPosts(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.category1 = Category.objects.create(title='Category 1')
        self.category2 = Category.objects.create(title='Category 2')
        self.news1 = News.objects.create(title='Test news 1', content='Test content 1',
                                         category=self.category1,
                                         photo=SimpleUploadedFile("avatar.jpg", b'file_content',
                                                                  content_type='image/jpeg'))
        self.news2 = News.objects.create(title='Test news 2', content='Test content 2',
                                         category=self.category2,
                                         photo=SimpleUploadedFile('avatar.jpg', b'file_content',
                                                                  content_type='image/jpeg'))

    def test_get_all_posts_with_search(self):
        response = self.client.get(self.url, {'search': 'Test news 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test news 1')
        self.assertNotContains(response, 'Test news 2')

    def test_get_all_posts_without_search(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test news 1')
        self.assertContains(response, 'Test news 2')


class TestShowOnePost(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='Category 1')
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com',
                                             password='testpassword123', first_name='Dima', last_name='Dimov',
                                             avatar=SimpleUploadedFile('avatar.jpg', b'file_content',
                                                                       content_type='image/jpeg'))
        self.news1 = News.objects.create(title='Test news 1', content='Test content 1',
                                         category=self.category1, author=self.user,
                                         photo=SimpleUploadedFile('avatar.jp', b'file_content',
                                                                  content_type='image/jpeg'), slug='testnews1')
        self.comment1 = Comment.objects.create(user=self.user, post=self.news1, content='Test comment')

    def test_show_one_post(self):
        response = self.client.get(reverse('one_post', args=[self.news1.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test news 1')
        self.assertContains(response, 'Test content 1')

    def test_post_comment(self):
        user = User.objects.create_user(username='testuser1', password='12345')
        self.client.login(username='testuser1', password='12345')
        data = {'content': 'New comment'}
        response = self.client.post(reverse('one_post', args=[self.news1.slug]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.last().content, 'New comment')
