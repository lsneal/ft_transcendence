path "database/static-creds/my-rolev1"
{
    capabilities = ["read"]
}

path "kv/*" 
{
    capabilities = ["create", "read"]
}