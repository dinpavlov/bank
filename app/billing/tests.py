from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Account


class AccountApiTests(APITestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='banktest@bank.com',
            password='testpass1_1',
            username='test_1'
        )
        self.client = APIClient()
        self.account = Account.objects.create(
            account_name = 'test_account',
            overdraft=False)

    def test_get_account(self):
        res = self.client.get(reverse('billing:account_get', args=[self.account.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        data = {
            "account_name": self.account.account_name,
            "overdraft": True
        }
        res = self.client.post(reverse('billing:account_create'), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(id=res.data['id'])
        for key in data.keys():
            self.assertEqual(data[key], getattr(account, key))

    def test_create_default_overdraft_account(self):
        data = {
            "account_name": self.account.account_name,
        }
        res = self.client.post(reverse('billing:account_create'), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(id=res.data['id'])
        for key in data.keys():
            self.assertEqual(data[key], getattr(account, key))