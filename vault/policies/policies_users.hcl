path "database/+/postgres_users"
{
    capabilities = ["create", "read", "update"] 
}

path "kv/django_secrets_users" 
{
    capabilities = ["create", "read"]
}