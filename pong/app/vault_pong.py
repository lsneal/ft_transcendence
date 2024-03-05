import hvac
import os 

VAULT_ADDR='http://vault:8200'

token_file_path = "/opt/pong_token"

with open(token_file_path, "r") as file:
    VAULT_TOKEN = file.read().strip()

vault_client = hvac.Client(url='http://vault:8200', token=VAULT_TOKEN)

vault_client.secrets.database.configure(
    name='postgres_pong',
    plugin_name='postgresql-database-plugin',
    allowed_roles='postgres_pong',
    connection_url=f'postgresql://{{{{username}}}}:{{{{password}}}}@postgres_pong:5433/postgres?sslmode=disable',
    username='postgres',
    password='password',
)

vault_client.secrets.database.rotate_root_credentials(
    name='postgres_pong',
    mount_point='database'
)

rotation_statement = ["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"]

credentials = vault_client.secrets.database.create_static_role(
    name='postgres_pong',
    db_name='postgres_pong',
    username='django',
    rotation_statements=rotation_statement,
    rotation_period=3600,
    mount_point='database'
)

print('Configure Done Pong')
