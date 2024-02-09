

storage "raft" {
  path = "/etc/vault.d/file"
  node_id = "node1"
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = "true"
}

ui = true
api_addr = "http://127.0.0.1:8200"
cluster_addr = "http://127.0.0.1:8201"
disable_mlock = true