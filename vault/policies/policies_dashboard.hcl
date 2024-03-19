path "database/+/postgres_dashboard"
{
    capabilities = ["create", "read", "update"] 
}

path "database/+/devops_dashboard"
{
    capabilities = ["create", "read", "update"] 
}

path "kv/django_secrets_dashboard" 
{
    capabilities = ["create", "read"]
}