from django.test import TestCase
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user
        )

    def test_string_representation(self):
        #post = Post(title='asdasdasd')
        self.assertEqual(str(self.post), self.post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_content(self):
        self.assertEqual(self.post.title, 'A good title')
        self.assertEqual(f'{self.post.body}', 'Nice body content')
        self.assertEqual(f'{self.post.author}', 'testuser')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        no_response = self.client.get(reverse('post_detail', args=[123123]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{'title':'New title',
                                                         'body':'New text',
                                                         'author':self.user})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args=[1]), {'title': 'Updated title',
                                                                     'body': 'Updated text'})
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)