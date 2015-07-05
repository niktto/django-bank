# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db import models
from django.db.models import Sum

from ..locks import Locked
from ..exceptions import AccountNotEnoughResources
from .transaction import Transaction


class Account(models.Model):

    """Model class for ann Account - used to group Transactions and Locks."""

    name = models.CharField(max_length=255)

    @staticmethod
    def validate_value(value):
        if not isinstance(value, (int, Decimal, str)):
            raise ValueError('Value need to be a string, integer or Decimal.')
        return Decimal(value)

    def register_income(self, value, title):
        value = self.validate_value(value)
        if value <= Decimal('0'):
            raise ValueError(
                'Value need to be positive number, not %s' % value
            )

        return self._create_transaction(value, title)

    def _create_transaction(self, value, title):
        return Transaction.objects.create(
            account=self,
            title=title,
            value=value
        )

    def register_expense(self, value, title, current_lock=None):
        value = self.validate_value(value)
        if value >= Decimal('0'):
            raise ValueError(
                'Value need to be negative number, not %s' % value
            )

        if current_lock is not None:
            if current_lock.account != self:
                raise ValueError('Lock not for this account!')

            if self.balance >= value:
                return self._create_transaction(value, title)
            else:
                raise AccountNotEnoughResources(
                    'Not enough resources to register expense of %s' % value
                )

        with Locked(self):
            if self.balance >= value:
                return self._create_transaction(value, title)
            else:
                raise AccountNotEnoughResources(
                    'Not enough resources to register expense of %s' % value
                )

    @property
    def balance(self):
        return self.transaction_set.aggregate(Sum('value'))['value__sum']
