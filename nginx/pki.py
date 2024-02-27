import os
import hvac

token_file_path = "/opt/n_token"

with open(token_file_path, "r") as file:
    TOKEN = file.read().strip()

client = hvac.Client(url='http://vault:8200', token=TOKEN)

def generate_root_certif():

    generate_root_response = client.secrets.pki.generate_root(
        type='exported',
        common_name='New root CA'
    )
    root_private_key = generate_root_response['data']['private_key']
    root_cert = generate_root_response['data']['certificate']
    return root_cert

def generate_intermediate_certif():

    generate_intermediate_response = client.secrets.pki.generate_intermediate(
        type='exported',
        common_name='Vault integration tests'
    )
    intermediate_csr = generate_intermediate_response['data']['csr']
    intermediate_private_key = generate_intermediate_response['data']['private_key']

    return intermediate_csr

def sign_intermediate_certif(intermediate_csr):
    sign_intermediate_response = client.secrets.pki.sign_intermediate(
        csr=intermediate_csr,
        common_name='localhost'
    )
    signed_intermediate_cert = sign_intermediate_response['data']['issuing_ca']

    return signed_intermediate_cert

#renewal_options = {
#    'ttl': '30s',
#    'renewal': '1m',
#    'renewal_grace_period': '1m'
#}

create_or_update_role_response = client.secrets.pki.create_or_update_role(
    'pki_cert_role',
    {
        'ttl': '30s',
        'renewal': '1m',
        'renewal_grace_period': '1m',
        'allow_localhost': 'true',
        'enforce_hostnames': 'false'
    }
)

def generate_final_certif():

    generate_certificate_response = client.secrets.pki.generate_certificate(
        name='pki_cert_role',
        common_name='localhost'
    )
    private_key = generate_certificate_response['data']['private_key']
    final_certif = generate_certificate_response['data']['certificate']
    
    certificate_file_path = "/opt/server.key"
    with open(certificate_file_path, "w") as file:
        file.write(private_key)

    certificate_file_path = "/opt/server.crt"
    with open(certificate_file_path, "w") as file:
        file.write(final_certif) 

    return (final_certif)

root_cert = generate_root_certif()

cert_intermediate = generate_intermediate_certif()
sign_intermediate_certif(cert_intermediate)

final_cert = generate_final_certif()
print("Certificate create")