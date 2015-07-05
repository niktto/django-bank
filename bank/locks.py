from django.db.utils import IntegrityError

from .exceptions import AccountLocked
from .models import lock


class Locked(object):

    def __init__(self, account):
        self.account = account
        self.lock = None
        super(Locked, self).__init__()

    def __enter__(self):
        try:
            self.lock = lock.AccountLock.objects.create(account=self.account)
        except IntegrityError:
            raise AccountLocked('Account %s already locked' % self.account.pk)
        return self.lock

    def __exit__(self, exc_type, value, trace_back):
        self.lock.delete()
