from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post, PostUser, Subscription
from users.models import User


class PostTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', password='test')
        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(title='test', text='test', blog=self.user.blog)

    def test_create(self):
        response = self.client.post(
            reverse('blog:add_post'),
            data={'title': 'title', 'text': 'text'}
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json(),
                          {
                              "title": "title",
                              "text": "text"
                          })

    def test_delete(self):
        response = self.client.delete(
            reverse('blog:delete_post', args=[self.post.id]),
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.first_user = User.objects.create(email='test@test.ru', password='test')
        self.client.force_authenticate(user=self.first_user)

        self.second_user = User.objects.create(email='test1@test.ru', password='test1')

    def test_create(self):
        response = self.client.post(
            reverse('blog:follow'),
            data={'blog': self.second_user.blog.id}
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json(),
                          {
                              'blog': self.second_user.blog.id
                          })

        response_error = self.client.post(
            reverse('blog:follow'),
            data={'blog': self.second_user.blog.id}
        )

        self.assertEquals(response_error.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(response_error.json(),
                          {
                              "non_field_errors": [
                                  "Вы уже подписаны на этот блог"
                              ]
                          })

    def test_delete(self):
        subscription = Subscription.objects.create(blog=self.second_user.blog, user=self.first_user)

        response = self.client.delete(
            reverse('blog:unfollow', args=[subscription.id]),
            headers={"Content-Type": "application/json"}
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class PostUserTestCase(APITestCase):

    def setUp(self):
        self.first_user = User.objects.create(email='test@test.ru', password='test')
        self.client.force_authenticate(user=self.first_user)

        self.second_user = User.objects.create(email='test1@test.ru', password='test1')
        self.post = Post.objects.create(title='test', text='test', blog=self.second_user.blog)

    def test_create(self):
        response = self.client.post(
            reverse('blog:mark_read_post'),
            data={'post': self.post.id}
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json(),
                          {
                              'post': self.post.id
                          })

        response_error = self.client.post(
            reverse('blog:mark_read_post'),
            data={'post': self.post.id}
        )

        self.assertEquals(response_error.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(response_error.json(),
                          {
                              "non_field_errors": [
                                  "Вы уже отметили на этот пост прочитанным"
                              ]
                          })

    def test_delete(self):
        post_user = PostUser.objects.create(post=self.post, user=self.first_user)

        response = self.client.delete(
            reverse('blog:mark_unread_post', args=[post_user.id]),
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class PostListTestCase(APITestCase):

    def setUp(self):
        self.first_user = User.objects.create(email='test@test.ru', password='test')
        self.second_user = User.objects.create(email='test1@test.ru', password='test1')
        self.third_user = User.objects.create(email='test2@test.ru', password='test2')
        self.fourth_user = User.objects.create(email='test3@test.ru', password='test3')

        self.first_subscription = Subscription.objects.create(blog=self.second_user.blog, user=self.first_user)
        self.second_subscription = Subscription.objects.create(blog=self.third_user.blog, user=self.first_user)

        self.first_post = Post.objects.create(title='test1', text='test1', blog=self.second_user.blog)
        self.second_post = Post.objects.create(title='test2', text='test2', blog=self.second_user.blog)
        self.third_post = Post.objects.create(title='test3', text='test3', blog=self.second_user.blog)
        self.fourth_post = Post.objects.create(title='test4', text='test4', blog=self.third_user.blog)
        self.fifth_post = Post.objects.create(title='test5', text='test5', blog=self.fourth_user.blog)

        self.client.force_authenticate(user=self.first_user)

    def test_list(self):
        response = self.client.get(
            reverse('blog:posts_list'),
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json().get('count'), 4)
        self.assertEquals(response.json().get('next'), None)
        self.assertEquals(response.json().get('previous'), None)
        self.assertEquals(response.json().get('results')[0].get('id'), self.fourth_post.id)
        self.assertEquals(response.json().get('results')[1].get('id'), self.third_post.id)
        self.assertEquals(response.json().get('results')[2].get('id'), self.second_post.id)
        self.assertEquals(response.json().get('results')[3].get('id'), self.first_post.id)
        self.assertEquals(tuple(response.json().get('results')[1].keys()),
                          ('id', 'title', 'text', 'created_at', 'blog'))
