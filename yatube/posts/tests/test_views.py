import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.image = uploaded
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='test',
            slug='test',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            image=cls.image,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage_template(self):
        """Страница 'posts:index' использует шаблон posts/index.html."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_page_template(self):
        """
        Страница по адресу 'posts:group_list'
        использует шаблон posts/group_list.html.
        """
        url = reverse('posts:group_list', kwargs={'slug': self.group.slug})
        response = self.authorized_client.get(url)
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_page_template(self):
        """
        Страница по адресу 'posts:profile'
        использует шаблон posts/profile.html.
        """
        url = reverse('posts:profile', kwargs={'username': self.user.username})
        response = self.authorized_client.get(url)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_page_template(self):
        """
        Страница по адресу 'posts:post_detail'
        использует шаблон posts/post_detail.html.
        """
        url = reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        response = self.authorized_client.get(url)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_create_page_template(self):
        """
        Страница по адресу 'posts:post_create'
        использует шаблон posts/create_post.html.
        """
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_edit_page_template(self):
        """
        Страница по адресу 'posts:post_edit'
        использует шаблон posts/create_post.html.
        """
        url = reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        response = self.authorized_client.get(url)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_index_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом"""
        image = self.post.image
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context.get('page_obj')[0], self.post)
        self.assertEqual(response.context.get('page_obj')[0].image, image)

    def test_group_posts_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом"""
        url = reverse('posts:group_list', kwargs={'slug': self.group.slug})
        image = self.post.image
        response = self.authorized_client.get(url)
        self.assertEqual(response.context.get('group'), self.group)
        self.assertEqual(response.context.get('page_obj')[0].image, image)

    def test_profile_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом"""
        url = reverse('posts:profile', kwargs={'username': self.user})
        image = self.post.image
        response = self.authorized_client.get(url)
        self.assertEqual(response.context.get('author'), self.user)
        self.assertEqual(response.context.get('page_obj')[0].image, image)

    def test_post_detail_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом"""
        url = reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        image = self.post.image
        response = self.authorized_client.get(url)
        self.assertEqual(response.context.get('post').id, self.post.id)
        self.assertEqual(response.context.get('post').image, image)

    def test_edit_post_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом"""
        url = reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        response = self.authorized_client.get(url)
        self.assertEqual(response.context.get('post').id, self.post.id)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='test',
            slug='test',
        )
        Post.objects.bulk_create([
            Post(text='1', author=cls.user, group=cls.group),
            Post(text='2', author=cls.user, group=cls.group),
            Post(text='3', author=cls.user, group=cls.group),
            Post(text='4', author=cls.user, group=cls.group),
            Post(text='5', author=cls.user, group=cls.group),
            Post(text='6', author=cls.user, group=cls.group),
            Post(text='7', author=cls.user, group=cls.group),
            Post(text='8', author=cls.user, group=cls.group),
            Post(text='9', author=cls.user, group=cls.group),
            Post(text='10', author=cls.user, group=cls.group),
            Post(text='11', author=cls.user, group=cls.group),
            Post(text='12', author=cls.user, group=cls.group),
            Post(text='13', author=cls.user, group=cls.group),
        ])

# from django.db import transaction
#         with transaction.atomic():
#             for i in range(13):
#                 Post.objects.create(
#                     text=i,
#                     author=cls.user,
#                     group=cls.group)

# В интернетах наткнулся еще на такой способ
# множествееного создания записей в ДБ
# Можно использовать его или bulk_create() эффективнее?

    def setUp(self):
        cache.clear()
        self.guest_client = Client()

    def test_first_index_page_contains_ten_records(self):
        """Количество постов на первой странице ровно 10'"""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_index_page_contains_three_records(self):
        """Количество постов на второй странице ровно 3"""
        response = self.guest_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_group_page_contains_ten_records(self):
        """Количество постов на первой странице ровно 10"""
        url = reverse('posts:group_list', kwargs={'slug': self.group.slug})
        response = self.guest_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_group_page_contains_three_records(self):
        """Количество постов на второй странице ровно 3"""
        group_slug = self.group.slug
        page2 = '?page=2'
        url = reverse('posts:group_list', kwargs={'slug': group_slug}) + page2
        response = self.guest_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_profile_page_contains_ten_records(self):
        """Количество постов на первой странице ровно 10"""
        username = self.user.username
        url = reverse('posts:profile', kwargs={'username': username})
        response = self.guest_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_profile_page_contains_three_records(self):
        """Количество постов на второй странице ровно 3"""
        username = self.user.username
        page2 = '?page=2'
        url = reverse('posts:profile', kwargs={'username': username}) + page2
        response = self.guest_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 3)


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_one = User.objects.create_user(username='user_one')
        cls.user_two = User.objects.create_user(username='user_two')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user_two,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_one)

    def test_follow(self):
        """Авторизованный пользователь может подписываться на других"""
        follow_url = f'/profile/{self.user_two.username}/follow/'
        unfollow_url = f'/profile/{self.user_two.username}/unfollow/'
        self.authorized_client.get(follow_url)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user_one,
                author=self.user_two,
            ).exists())
        self.authorized_client.get(unfollow_url)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user_one,
                author=self.user_two,
            ).exists())

    def test_follow_index(self):
        follow_url = f'/profile/{self.user_two.username}/follow/'
        self.authorized_client.get(follow_url)
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertEqual(response.context.get('page_obj')[0], self.post)
