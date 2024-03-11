path "kv/*" 
{
    capabilities = ["read"]
}

path "database/+/postgres_users"
{
    capabilities = ["create", "read", "update"] 
}

path "database/+/postgres_pong"
{
    capabilities = ["create", "read", "update"] 
}