import unittest
from django.test import TestCase, Client
from django.urls import reverse, resolve

from .models import Profile, Relationship, Post, User
from network.views import index, login_view, logout_view, register, edit, profile, following, like


class PostTestCase(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create(username='username', email='username@test.com', password='password')

        # create profile
        self.profile = Profile.objects.create(user=self.user)

    def test_post_is_valid(self):
        post = Post.objects.create(author=self.profile, content="some content")
        self.assertTrue(post.is_valid_post())

    def test_post_is_invalid(self):
        post = Post.objects.create(author=self.profile, content="")
        self.assertFalse(post.is_valid_post())

    def test_likes_count(self):
        post = Post.objects.create(author=self.profile, content="some content")
        post.likes.add(self.profile)
        self.assertEqual(post.likes.count(), 1)


class ProfileTestCase(TestCase):
    def setUp(self):
        # create users
        self.user1 = User.objects.create(username='username', email='username@test.com', password='password')
        self.user2 = User.objects.create(username='username2', email='username2@test.com', password='password2')

        # create profiles
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

        self.profile1.add_relationship(self.profile2)

    def test_add_relationship(self):
        self.assertEqual(self.profile1.relationships.count(), 1)

    def test_get_followers(self):
        self.assertEqual(len(list(self.profile2.get_followers())), 1)

    def test_get_following(self):
        self.assertEqual(len(list(self.profile1.get_following())), 1)

    def test_delete_relationship(self):
        self.profile1.delete_relationship(self.profile2)
        self.assertEqual(self.profile1.relationships.count(), 0)


class TestUrls(TestCase):
    def test_index_url_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_login_url_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_register_url_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_edit_url_resolved(self):
        url = reverse('edit', args=['1'])
        self.assertEqual(resolve(url).func, edit)

    def test_profile_url_resolved(self):
        url = reverse('profile', args=['1'])
        self.assertEqual(resolve(url).func, profile)

    def test_index_url_resolved(self):
        url = reverse('following')
        self.assertEqual(resolve(url).func, following)

    def test_index_url_resolved(self):
        url = reverse('like')
        self.assertEqual(resolve(url).func, like)


class WebpageTests(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='username@test.com', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.client = Client()
        self.client.login(username='username', password='password')
        self.post1 = Post.objects.create(author=self.profile, content="something")
        self.post2 = Post.objects.create(author=self.profile, content="something 2")

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
