import hvac
import os

class creds():
    database_credentials =''

    def init(val):
        if val == 1:
            VAULT_ADDR = 'http://vault:8200'
            fd = os.open("/opt/token", os.O_RDONLY)
            n_bytes = 95 # token size
            TOKEN = os.read(fd, n_bytes)

            vault_client = hvac.Client(url='http://vault:8200', token=TOKEN)
            database_credentials = vault_client.read('database/creds/my-rolev1')
            return database_credentials['data']['username']
        else:
            return database_credentials['data']['password']


# create