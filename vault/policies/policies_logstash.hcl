path "kv/elasticsearch" 
{
    capabilities = ["read"]
}

path "database/+/postgres_users"
{
    capabilities = ["read"] 
}

path "database/+/postgres_pong"
{
    capabilities = ["read"] 
}