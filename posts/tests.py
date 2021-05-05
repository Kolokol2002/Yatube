from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()

class ProfileTest(TestCase):
    def setUp(self):
        # создаём пользователя
        self.client = Client()
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        # создаём пост от имени пользователя
        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user)

    def test_profile(self):
        #После регистрации пользователя создается его персональная страница (profile)
        response = self.client.get("/sarah/")
        self.assertEqual(response.status_code, 200)
        #После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице
        #пользователя (profile), и на отдельной странице поста (post)
        self.assertEqual(response.context["prof"][0], self.post)
        response = self.client.get("")
        self.assertEqual(response.context["post_list"][0], self.post)

    def test_new_post(self):
        #Авторизованный пользователь может опубликовать пост (new)
        #Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
        self.client.login(username=self.user, password="12345")
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200)

        self.client.post('/new/',
                         data={
                             "text": "Тест для створення нового поста"
                         }
                         )
        self.assertTrue(Post.objects.filter(text='Тест для створення нового поста',
                                            author=self.user).exists()
                        )
        self.client.logout()
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 302)

    def test_edit_post(self):
        #Авторизованный пользователь может отредактировать свой пост
        # и его содержимое изменится на всех связанных страницах
        self.client.login(username=self.user, password="12345")
        response = self.client.get(f'/{self.user}/{self.post.id}/edit/')
        self.assertEqual(response.status_code, 200)
        self.client.post(f'/{self.user}/{self.post.id}/edit/',
                         data={
                             'text': 'Змінено для тесту',

                         }
                         )
        self.assertTrue(Post.objects.filter(text='Змінено для тесту').exists())

class ErrorsTest(TestCase):
    def test_404(self):
        response = self.client.get("/test/test/test/test/")
        self.assertEqual(response.status_code, 404)




