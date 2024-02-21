import hvac
import requests
import os

def init_server():

    #fd = os.open('/opt/token', os.O_RDONLY)
    #n_bytes = 95
    #TOKEN = os.read(fd, n_bytes)

    #print(TOKEN)

    client = hvac.Client(url='http://vault:8200', token='hvs.2T9aAGC4Yv6Y5ggBGwDFXIeg')

    #database_credentials = client.read('database/creds/my-rolev1')
    database_credentials = client.read('kv/django_secrets')
#    print(database_credentials)
    print(database_credentials['data']['django_key'])
    #print(client.is_authenticated())

init_server()
