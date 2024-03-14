import hvac
import os 

VAULT_ADDR='http://vault:8200'

token_file_path = "/opt/pong_token"

with open(token_file_path, "r") as file:
    VAULT_TOKEN = file.read().strip()

vault_client = hvac.Client(url='http://vault:8200', token=VAULT_TOKEN)

rotation_statement = ["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"]

vault_client.secrets.database.configure(
    name='postgres_pong',
    plugin_name='postgresql-database-plugin',
    allowed_roles='*',
    connection_url=f'postgresql://{{{{username}}}}:{{{{password}}}}@postgres_pong:5433/postgres?sslmode=disable',
    username='postgres',
    password='password',
)

# devops user
vault_client.secrets.database.create_static_role(
    name='devops_pong',
    db_name='postgres_pong',
    username='logstash',
    rotation_statements=rotation_statement,
    mount_point='database'
)

vault_client.secrets.database.rotate_root_credentials(
    name='postgres_pong',
    mount_point='database'
)

# django user
vault_client.secrets.database.create_static_role(
    name='postgres_pong',
    db_name='postgres_pong',
    username='django',
    rotation_statements=rotation_statement,
    rotation_period=3600,
    mount_point='database'
)

print('Configure Done Pong')
