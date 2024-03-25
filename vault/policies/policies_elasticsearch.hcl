path "kv/elasticsearch" 
{
    capabilities = ["read"]
}

path "kv/kibana" 
{
    capabilities = ["read"]
}

path "sys/mounts/*" 
{  
    capabilities = [ "create", "read", "update", "delete", "list" ]
}

# List enabled secrets engine
path "sys/mounts" 
{
  capabilities = [ "read", "list" ]
}

# Work with pki secrets engine
path "pki*" 
{
  capabilities = [ "create", "read", "update", "delete", "list" ]
}
