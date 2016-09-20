from django.db import models
import uuid

from accounts.models import Account

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    office_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    url = models.CharField(max_length=255)
    account = models.ForeignKey(Account, related_name = 'files')
    
    def dict(self):
        return {
            'id': self.office_id,
            'name': self.name,
            'created': self.created.isoformat(),
            'modified': self.modified.isoformat(),
            'url': self.url,
            'account_id': str(self.account.id),
        }