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

    

