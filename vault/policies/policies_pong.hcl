path "database/+/postgres_pong"
{
    capabilities = ["create", "read", "update"] 
}

path "kv/*" 
{
    capabilities = ["create", "read"]
}