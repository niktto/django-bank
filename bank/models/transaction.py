# -*- coding: utf-8 -*-
from django.db import models


class Transaction(models.Model):

    """Model for Transactions on an Account."""

    title = models.CharField(max_length=255)

    account = models.ForeignKey('Account')

    value = models.DecimalField(max_digits=10, decimal_places=4)

    is_pending = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    confirmed_at = models.DateTimeField(null=True, blank=True)
