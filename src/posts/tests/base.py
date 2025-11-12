from django.test import TestCase
from posts.models import Post,User
from django.urls import reverse

header = 'header test1'
body = 'body test1'    
def create_post(user, header=header, body= body, amount=1):
    if amount ==1:
        post_obj = Post.objects.create(user=user, header=header, body=body)
        return post_obj
    
    posts= [Post(user= user, header= header, body=body) for _ in range(0,amount)]
    post_objects = Post.objects.bulk_create(posts)
    return post_objects


class UserAndPostFactoryMixin:
    # note to myself: setUpTestData runs once before every class that inherits from TestCase
    # but setUp() runs once before every method!
    
    @classmethod
    def setUpTestData(cls): 
        cls.user1 = User.objects.create_user(email='user1@gmail.com',
                                             username='user1', password='1234')
        cls.user2 = User.objects.create_user(email='user2@gmail.com',
                                             username='user2', password='1234')

        # create single objects (create_post(amount=1) returns the object)
        cls.post_obj1 = create_post(user=cls.user1)
        cls.post_obj2 = create_post(user=cls.user2,
                                    header='header test2', body='body test2')

class SignUpMixin:
    def sign_up(self, email='test@gmail.com', username='test', password= 'test',captcha_1= 'passed'):
        response = self.client.post(reverse('sign_up'),
                                    data={'email': email,
                                        'username':username,
                                        'password':password,
                                        'captcha_0': 'dummy',
                                        'captcha_1':captcha_1})
        return response