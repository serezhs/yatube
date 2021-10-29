from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, Comment, Follow

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def test_post_model_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_post = str(post)
        self.assertEqual(expected_post, 'Тестовая группа')


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_model_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = GroupModelTest.group
        expected_group = str(group)
        self.assertEqual(expected_group, 'Тестовая группа')


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тест',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Test',
        )

    def test_comment_model_have_correct_object_names(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        comment = CommentModelTest.comment
        expected_comment = str(comment)
        self.assertEqual(expected_comment, 'Test')


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.author = User.objects.create_user(username='author')
        cls.following = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def test_follow_model_have_correct_object_names(self):
        """Проверяем, что у модели Follow корректно работает __str__."""
        follow = FollowModelTest.following
        expected_follow = str(follow)
        self.assertEqual(expected_follow, 'user following author')
