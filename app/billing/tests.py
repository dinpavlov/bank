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

class TransferApiTests(APITestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='banktest@bank.com',
            password='testpass1_1',
            username='test_1'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.from_overdraft_account = Account.objects.create(
            account_name = 'test_from_account',
            overdraft=True
            )
        self.to_account = Account.objects.create(
            account_name = 'test_to_account',
            overdraft=False
            )
        self.amount = 1000

    def test_transfer_from_overdraft(self):
        payload = {
            "from_account": self.from_overdraft_account.id,
            "to_account": self.to_account.id,
            "amount": self.amount
            }
        res = self.client.post(reverse('billing:transfer_create'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        to_account = Account.objects.get(id=self.to_account.id)
        from_overdraft_account = Account.objects.get(id=self.from_overdraft_account.id)
        self.assertEqual(self.to_account.balance + self.amount, to_account.balance)
        self.assertEqual(self.from_overdraft_account.balance - self.amount, from_overdraft_account.balance)