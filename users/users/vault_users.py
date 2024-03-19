import hvac
import os 

VAULT_ADDR='http://vault:8200'

token_file_path = "/opt/users_token"

with open(token_file_path, "r") as file:
    VAULT_TOKEN = file.read().strip()

vault_client = hvac.Client(url='http://vault:8200', token=VAULT_TOKEN)

rotation_statement = ["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"]

vault_client.secrets.database.configure(
    name='postgres_users',
    plugin_name='postgresql-database-plugin',
    allowed_roles='*',
    connection_url=f'postgresql://{{{{username}}}}:{{{{password}}}}@postgres_users:5432/postgres?sslmode=disable',
    username='postgres',
    password='password',
)

# devops user
credentials = vault_client.secrets.database.create_static_role(
    name='devops_users',
    db_name='postgres_users',
    username='devops',
    rotation_statements=rotation_statement,
    mount_point='database'
)

vault_client.secrets.database.rotate_root_credentials(
    name='postgres_users',
    mount_point='database'
)

# django user
credentials = vault_client.secrets.database.create_static_role(
    name='postgres_users',
    db_name='postgres_users',
    username='django',
    rotation_statements=rotation_statement,
    rotation_period=3600,
    mount_point='database'
)

print('Configure Done Users')
