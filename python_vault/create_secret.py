import hvac
import json

def write_secret():

    client = hvac.Client(url='http://127.0.0.1:8200')
    create_response = client.secrets.kv.v2.create_or_update_secret(path='cubbyhole', secret=dict(FOO="eve2"))

    print (json.dumps(create_response, indent=4, sort_keys=True))

write_secret()
