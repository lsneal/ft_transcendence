path "database/+/postgres_pong"
{
    capabilities = ["create", "read", "update"] 
}

path "kv/django_secrets_pong" 
{
    capabilities = ["create", "read"]
}