import requests

def handle_oauth_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}
    return wrapper

class connectedClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_to_api(self, endpoint):
        return requests.get(endpoint, headers={
            'Authorization': 'Bearer ' + self.access_token
        }).json()

class OAuth2Client:
    def __init__(self, client_id, client_secret, redirect_uri, auth_endpoint, token_endpoint):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
    def _get_auth_url(self, **params):
        default_params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        default_params.update(params)
        return self.auth_endpoint + '?' + '&'.join(f"{k}={v}" for k, v in default_params.items())
    def _exchange_for_token(self, code):
        return requests.post(self.token_endpoint, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }).json()
    def _refresh_for_token(self, refresh_token):
        return requests.post(self.token_endpoint, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'refresh_token'
        }).json()
        
class AuthorizationCodeClient(OAuth2Client):
    @handle_oauth_errors
    def get_authorization_url(self, **params):
        return self._get_auth_url(response_type='code', **params)
    @handle_oauth_errors
    def get_token(self, code):
        return self._exchange_for_token(code)
    def refresh_token(self, refresh_token):
        return super()._refresh_for_token(refresh_token)
    
   
class ImplicitClient(OAuth2Client):
    @handle_oauth_errors
    def get_authorization_url(self, **params):
        return self._get_auth_url(response_type='token', **params)
    
class ClientCredentialsClient(OAuth2Client):
    @handle_oauth_errors
    def get_token(self):
        response = requests.post(self.token_endpoint, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        })
        return response.json()
    
class getInfoClient(connectedClient):
    def get_name_client(self, endpoint):
        return self.get_to_api(endpoint)

    
#creds = ClientCredentialsClient(
#    client_id="u-s4t2ud-11f2f99d539fd7e0882f03a1a9d8956a5e81f1122575411181eff146d684e7f3",
#    client_secret="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",
#    redirect_uri="https%3A%2F%2Flocalhost%2F",
#    auth_endpoint="https://api.intra.42.fr/oauth/authorize",
#    token_endpoint="https://api.intra.42.fr/oauth/token"
#)
#    
## Define your OAuth2 client
#client = AuthorizationCodeClient(
#    client_id="u-s4t2ud-11f2f99d539fd7e0882f03a1a9d8956a5e81f1122575411181eff146d684e7f3",
#    client_secret="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",
#    redirect_uri="https://localhost/",
#    auth_endpoint="https://api.intra.42.fr/oauth/authorize",
#    token_endpoint="https://api.intra.42.fr/oauth/token"
#)

# Get the authorization URL and redirect the user

#auth_url = client.get_authorization_url()
#print(f"Redirect the user to: {auth_url}")
#
## After redirect, exchange the code for a token
#code = "c0ae6e6d1a0481b3883a349c6afddff15f82415c16571ece0d27c9439df7bd12"
#token_info = client.get_token(code)
#print(token_info)
