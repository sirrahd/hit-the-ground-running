from people.models import Person
import graph.ols

def add_connections_from_dict(account, people):
    response = []

    for person in people['value']:
        p = None                
        try:
            p = Person.objects.create(
                office_id = person['Id'],
                email = person['Email'],
                name = person['PreferredName'],
                account = account,
            )
        except: # The person was already created from another connection
            p = Person.objects.get(office_id=person['Id'])

        response.append(p)
        
    return response

def get_new_connections(account):
    r = graph.ols.get_relationships(account)
    connections = add_connections_from_dict(account, r)

    return connections