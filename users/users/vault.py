import hvac
import os 

VAULT_ADDR='http://vault:8200'

fd = os.open("/opt/token", os.O_RDONLY)
n_bytes = 95
VAULT_TOKEN = os.read(fd, n_bytes)

vault_client = hvac.Client(url='http://vault:8200', token=VAULT_TOKEN)

vault_client.secrets.database.configure(
    name='postgres_users',
    plugin_name='postgresql-database-plugin',
    allowed_roles='postgres_users',
    connection_url=f'postgresql://{{{{username}}}}:{{{{password}}}}@postgres_users:5432/postgres?sslmode=disable',
    username='postgres',
    password='password',
)

vault_client.secrets.database.rotate_root_credentials(
    name='postgres_users',
    mount_point='database'
)

rotation_statement = ["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';"]

credentials = vault_client.secrets.database.create_static_role(
    name='postgres_users',
    db_name='postgres_users',
    username='django',
    rotation_statements=rotation_statement,
    rotation_period=45,
    mount_point='database'
)