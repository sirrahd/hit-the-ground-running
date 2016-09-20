from files.models import File
import graph.ols

def add_connections_from_dict(account, files):
    response = []

    for file in files['value']:
        f = None                
        try:
            f = File.objects.create(
                office_id = file['Id'],
                name = file['Name'],
                created = file['DateTimeCreated'],
                modified = file['DateTimeLastModified'],
                url = file['WebUrl'],
                account = account,
            )
        except: # The person was already created from another connection
            f = File.objects.get(office_id=file['Id'])
            
        response.append(f)
        
    return response

def get_new_files(account):
    r = graph.ols.get_trending_files(account)
    connections = add_connections_from_dict(account, r)

    return connections