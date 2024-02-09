import hvac
import requests

def init_server():

    client = hvac.Client(url='http://vault:8200')
    print(client.is_authenticated())

init_server()
