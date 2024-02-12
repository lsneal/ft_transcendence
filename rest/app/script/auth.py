import hvac
import requests
import os

def init_server():

    fd = os.open('/opt/token', os.O_RDONLY)
    n_bytes = 28
    TOKEN = os.read(fd, n_bytes)

    print(TOKEN)

    client = hvac.Client(url='http://vault:8200', token='hvs.DhsCeJmj9KggeqA1URSPzQgx')

    #database_credentials = client.read('database/creds/my-rolev1')
    database_credentials = client.read('kv/django_secrets')
    print(database_credentials)
    print(database_credentials['data']['Value'])
    print(client.is_authenticated())

init_server()
