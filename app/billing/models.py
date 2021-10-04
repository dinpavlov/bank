from django.db import models
from django.conf import settings

# Create your models here.

class Account(models.Model):
    account_name = models.CharField(max_length=100)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    overdraft = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.id

class Transfer(models.Model):

    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='from_account'
    )

    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='to_account'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.id
