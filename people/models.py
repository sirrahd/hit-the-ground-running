from django.db import models
import uuid

from accounts.models import Account

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    office_id = models.UUIDField()
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    account = models.ForeignKey(Account, related_name = 'people')
    
    def dict(self):
        return {
            'id': str(self.office_id),
            'email': self.email,
            'name': self.name,
            'account': str(self.account.id),
        }