path "database/+/postgres_users"
{
    capabilities = ["create", "read", "update"] 
}

path "kv/*" 
{
    capabilities = ["create", "read"]
}