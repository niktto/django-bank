# -*- coding: utf-8 -*-
from django.db import models


class AccountLock(models.Model):

    """Model for lock in account operation locking mechanism."""

    account = models.ForeignKey('Account', unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
