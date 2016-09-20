from django.db import models
import base64

from graph.ols import get_my_info, get_relationships

class Account(models.Model):
    id = models.UUIDField(primary_key=True)
    tenant_id = models.UUIDField()
    alias = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    ols_token = models.CharField(max_length=255)
    graph_token = models.CharField(max_length=255)

    def logout(self, request):
        request.session.pop('userid', None)

    @classmethod
    def login(Account, request, email=None, password=None):
        if 'userid' in request.session: # Already logged in
            try:
                return Account.objects.get(id=request.session['userid'])
            except:
                request.session.pop('userid', None)
        
        ols_token = create_token(email, password)
        info = get_my_info(ols_token)

        if 'Id' in info: # Successful login
            id = info['Id'].split('@')[0]

            try:
                a = Account.objects.get(id=id)
                request.session['userid'] = id
            except: # Account doesn't exist locally yet
                a = Account.objects.create(
                    id = id,
                    tenant_id = info['Id'].split('@')[0],
                    alias = info['Alias'],
                    display_name = info['DisplayName'],
                    email = info['EmailAddress'],
                    ols_token = ols_token,
                )
                request.session['userid'] = id
            
            return a
        
        return None

def create_token(email, password):
    return base64.standard_b64encode('{}:{}'.format(email, password).encode('ascii')).decode('utf-8').replace('\n', '')