import uuid
import requests
import datetime
import json
graph_api_endpoint = 'https://graph.microsoft.com/beta{0}'

def make_api_call(method, url, token, payload = None, parameters = None):
    headers = {
        'User-Agent': 'hack/1.0',
        'Authorization': 'Bearer {0}'.format(token),
        'Accept': 'application/json',
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
    get_info_url = graph_api_endpoint.format('/me')

    r = make_api_call('GET', get_info_url, token)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return '{0}: {1}'.format(r.status_code, r.text)

def get_my_emails(account):
	aboutAWeekAgo = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')

	query = '/me/messages?$filter=ReceivedDateTime%20gt%20' + aboutAWeekAgo + "&$top=1000"
	get_my_emails_url = graph_api_endpoint.format(query)
	
	r = make_api_call('GET', get_my_emails_url, account.graph_token)
	
	if (r.status_code == requests.codes.ok):
		emails = r.json()
		myteam = account.people.all()
		relevant_emails = []
		for mail in emails['value']:
			if list_comp([mail['from']], myteam) or list_comp(mail['toRecipients'],myteam) or list_comp(mail['ccRecipients'],myteam):
				mail['body'] = ''
				relevant_emails.append(mail)

		emails['value'] = relevant_emails
        
		return emails
	else:
		return '{0}: {1}'.format(r.status_code, r.text)
		
def get_my_files(account):
	get_my_files_url = graph_api_endpoint.format('/me/drive/root/children')

	r = make_api_call('GET', get_my_files_url, account.graph_token)
	
	if (r.status_code == requests.codes.ok):
		return r.json()
	else:
		return '{0}: {1}'.format(r.status_code, r.text)

def get_my_calendar(account):
	get_my_calendar_url = graph_api_endpoint.format('/me/calendar')
	
	r = make_api_call('GET', get_my_calendar_url, account.graph_token)
	
	if (r.status_code == requests.codes.ok):
		return r.json()
	else:
		return '{0}: {1}'.format(r.status_code, r.text)

def list_comp(list1, list2):
	if list1 != [None] and list2 != [None]:
		for val1 in list1:
			for val2 in list2:
				if val1['emailAddress']['address'] == val2.email:
					return True
	return False
