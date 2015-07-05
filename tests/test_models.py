#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-bank
------------

Tests for `django-bank` models module.
"""

import unittest
from decimal import Decimal

from bank import models, locks, exceptions


class TestBank(unittest.TestCase):

    def setUp(self):
        self.account = models.Account(name="Testing account")
        self.account.save()

    def test_transaction_create(self):
        self.account.register_income(Decimal('10'), 'test')
        assert self.account.balance == Decimal('10')

    def test_transaction_both_ways(self):
        self.account.register_income(Decimal('10'), 'test')
        self.account.register_expense(Decimal('-9'), 'test')
        assert self.account.balance == Decimal('1')

    def test_transaction_lock_error(self):
        self.account.register_income(Decimal('10'), 'test')
        with locks.Locked(self.account):
            try:
                self.account.register_expense(Decimal('-9'), 'test')
            except exceptions.AccountLocked:
                assert self.account.balance == Decimal('10')
                return
            assert not 'No lock error happened!'

    def test_lock_passing(self):
        self.account.register_income(Decimal('10'), 'test')
        with locks.Locked(self.account) as lock:
            try:
                self.account.register_expense(
                    Decimal('-9'),
                    'test',
                    current_lock=lock
                )
            except exceptions.AccountLocked:
                assert not 'This test should share lock, something is wrong!'
            assert self.account.balance == Decimal('1')

    def tearDown(self):
        pass
