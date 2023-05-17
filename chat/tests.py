from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_jwt import utils
from rest_framework.test import APITestCase


class UserListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = utils.jwt_encode_handler(utils.jwt_payload_handler(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_users_list(self):
        url = reverse('chat:users_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChatWindowMessageListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = utils.jwt_encode_handler(utils.jwt_payload_handler(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_window_message(self):
        recipient_user = User.objects.create_user(username='recipient', password='testpassword')

        url = reverse('chat:window_message_list')
        data = {'user': recipient_user.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
