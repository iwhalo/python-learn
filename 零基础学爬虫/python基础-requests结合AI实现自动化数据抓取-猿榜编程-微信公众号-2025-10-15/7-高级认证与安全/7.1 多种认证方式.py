import requests
# 基本认证（Basic Auth）
from requests.auth import HTTPBasicAuth
r=requests.get('https://httpbin.org/get', auth=HTTPBasicAuth('username', 'password'))

# 简写形式
r=requests.get('https://httpbin.org/get',auth=('user','pass'))

########################################################################################################################

# 摘要认证（Digest Auth）
from requests.auth import HTTPDigestAuth
r=requests.get('https://httpbin.org/get',auth=HTTPDigestAuth('user','pass'))

########################################################################################################################

# OAuth1认证
from requests_oauthlib import OAuth1
auth=OAuth1(
    'YOUR_APP_KEY',
    'YOUR_APP_SECRET',
    'USER_OAUTH_TOKEN',
    'USER_OATUH_TOKEN_SECRET'
)
r=requests.get('https://api.twitter.com/1.1/account/verify_credentials.json',auth=auth)

########################################################################################################################

# OAuth2 认证
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# 客户端凭证模式
client=BackendApplicationClient(client_id='YOUR_CLIENT_IP')
oauth=OAuth2Session(client=client)
token=oauth.fetch_token(
    token_url='https://provider.com/oauth2/token',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET'
)
r=oauth.get('https://api.example.com/resource')

########################################################################################################################


# 自定义认证
class TokenAuth:
    """自定义令牌认证类"""
    def __init__(self,token):
        self.token=token

    def __call__(self, r):
        r.headers['Authorization']=f'Bearer {self.token}'
        return r

# 使用自定义认证
r=requests.get('https://api.example.com/protected',auth=TokenAuth('YOUR_TOKEN'))