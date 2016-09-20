import json
import uuid
import requests
import getpass
import base64
import datetime

outlook_api_endpoint = 'https://outlook.office365.com/api/beta{0}'

def make_api_call(method, url, token, payload = None, parameters = None):
    headers = {
        'Authorization': 'Basic {}'.format(token),
        'Content-Type': 'application/json',
    }

    request_id = str(uuid.uuid4())
    instrumentation = {
        'client-request-id': request_id,
        'return-client-request-id': 'true',
    }

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers = headers, params = parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({ 'Content-Type': 'application/json' })
        response = requests.patch(url, headers = headers, data = payload, params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type': 'application/json' })
        response = request.post(url, headers = headers, data = payload, params = parameters)

    return response

def get_my_info(token):
    get_info_url = outlook_api_endpoint.format('/me')

    r = make_api_call('GET', get_info_url, token)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return '{0}: {1}'.format(r.status_code, r.text)
        
def workingWith(account):
    people = []
    for i, person in enumerate(account.people.all()):
            
        people.append(person.dict())
    return people
    
def trendingAround(account):
    files = []
    for i, file in enumerate(account.files.all()):
            
        files.append(file.dict())
    return files

def get_relationships(account, userid=None):
    if not userid:
        get_relationships_url = outlook_api_endpoint.format('/me/workingWith')
    else:
        get_relationships_url = outlook_api_endpoint.format('/users/{0}/workingWith'.format(userid))

    r = make_api_call('GET', get_relationships_url, account.ols_token)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return '{0}: {1}'.format(r.status_code, r.text)

def get_my_calendar(account):
	get_my_calendar_url = outlook_api_endpoint.format('/me/calendar')
	
	r = make_api_call('GET', get_my_calendar_url, account.ols_token)
	
	if (r.status_code == requests.codes.ok):
		return r.json()
	else:
		return '{0}: {1}'.format(r.status_code, r.text)

def get_my_files(account):
	get_my_files_url = outlook_api_endpoint.format('/me/drives/root/children')

	r = make_api_call('GET', get_my_files_url, account.ols_token)
	
	if (r.status_code == requests.codes.ok):
		return r.json()
	else:
		return '{0}: {1}'.format(r.status_code, r.text)
		
def get_trending_files(account, userid=None):
    if not userid:
        get_relationships_url = outlook_api_endpoint.format('/me/trendingAround')
    else:
        get_relationships_url = outlook_api_endpoint.format('/users/{0}/trendingAround'.format(userid))

    r = make_api_call('GET', get_relationships_url, account.ols_token)

    if (r.status_code == requests.codes.ok):
        aboutAWeekAgo = datetime.datetime.now() - datetime.timedelta(days=7)
        files = r.json()
        recent_files = []
        for file in files['value']:
            if datetime.datetime.strptime(file['DateTimeLastModified'], '%Y-%m-%dT%H:%M:%SZ') > aboutAWeekAgo:
                recent_files.append(file)
        
        files['value'] = recent_files
        return files
    else:
        return '{0}: {1}'.format(r.status_code, r.text)
