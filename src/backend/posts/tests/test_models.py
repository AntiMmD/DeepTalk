from django.test import TestCase
from posts.models import Post
from .base import UserAndPostFactoryMixin

class UserAndPostModelsTest(UserAndPostFactoryMixin, TestCase):
    def test_each_post_is_associated_with_a_user(self):
        saved_post_obj1= Post.objects.get(user= self.user1 )
        saved_post_obj2= Post.objects.get(user= self.user2 )
        self.assertEqual(saved_post_obj1, self.post_obj1)
        self.assertEqual(saved_post_obj2,self. post_obj2)

    def test_post_has_a_created_at_field(self):
        self.assertGreater(self.post_obj2.created_at, self.post_obj1.created_at)