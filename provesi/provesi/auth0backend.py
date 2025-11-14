import requests
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings

class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture'),
    ]

    def authorization_url(self):
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        return details['user_id']

    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        return {
            'username': userinfo['nickname'],
            'first_name': userinfo['name'],
            'picture': userinfo['picture'],
            'user_id': userinfo['sub'],
        }

def getRole(request):
    user = request.user
    auth0user = user.social_auth.filter(provider="auth0")[0]
    accessToken = auth0user.extra_data['access_token']

    url = f'https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/userinfo'
    headers = {'authorization': f'Bearer {accessToken}'}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    namespace = settings.AUTH0_CUSTOM_NAMESPACE
    role = userinfo.get(f"{namespace}/role")
    print("ROL:", role) 
    return role


def getUserId(request):
    """Devuelve el sub de Auth0 (dueño lógico del pedido)."""
    user = request.user
    auth0user = user.social_auth.filter(provider="auth0")[0]
    accessToken = auth0user.extra_data['access_token']

    url = 'https://' + settings.SOCIAL_AUTH_AUTH0_DOMAIN + '/userinfo'
    headers = {'authorization': 'Bearer ' + accessToken}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()
    return userinfo["sub"]
