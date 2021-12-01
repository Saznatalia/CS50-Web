from django.test import TestCase

from .models import Profile, Relationship, Post, User

class PostTestCase(TestCase):
    def setUp(self):
        # create user
        user_1 = User.objects.create(username='username', email='username@test.com', password='password')
       
        # create profile
        profile_1 = Profile.objects.create(user=user_1)

        # create posts
        post1 = Post.objects.create(author=profile_1, content="some content")
        post2 = Post.objects.create(author=profile_1, content="")
    
    def test_post_is_valid(self):
        profile = Profile.objects.get(user=1)
        post = Post.objects.get(author=profile, content="some content")
        self.assertTrue(post.is_valid_post())

    def test_post_is_invalid(self):
        profile = Profile.objects.get(user=1)
        post = Post.objects.get(author=profile, content="")
        self.assertFalse(post.is_valid_post())

    def test_likes_count(self):
        profile = Profile.objects.get(user=1)
        post = Post.objects.get(author=profile, content="some content")
        post.likes.add(profile)
        self.assertTrue(post.likes.count(), 1)



class ProfileTestCase(TestCase):

    def setUp(self):
        # create users
        u1 = User.objects.create(username='username', email='username@test.com', password='password')
        u2 = User.objects.create(username='username2', email='username2@test.com', password='password2')

        # create profiles
        p1 = Profile.objects.create(user=u1)
        p2 = Profile.objects.create(user=u2)

        p1.add_relationship(p2)

    def test_add_relationship(self):
        p1 = Profile.objects.get(user=1)
        self.assertEqual(p1.relationships.count(), 1)

    def test_get_get_followers(self):
        p2 = Profile.objects.get(user=2)
        self.assertEqual(len(list(p2.get_followers())), 1)
    
    def test_get_following(self):
        p1 = Profile.objects.get(user=1)
        self.assertEqual(len(list(p1.get_following())), 1)

    def test_delete_relationshp(self):
        p1 = Profile.objects.get(user=1)
        p2 = Profile.objects.get(user=2)
        p1.delete_relationship(p2)
        self.assertEqual(p1.relationships.count(), 0)


