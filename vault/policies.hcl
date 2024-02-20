path "database/creds/my-rolev1"
{
    capabilities = ["create", "read"]
}

path "kv/*" 
{
    capabilities = ["create", "read"]
}