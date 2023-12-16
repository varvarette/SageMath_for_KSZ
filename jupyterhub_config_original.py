#version as of 06.11. without polishing 

import os
from oauthenticator.azuread import LocalAzureAdOAuthenticator, AzureAdOAuthenticator

#LocalAzureAdOAuthenticator: a version that mixes in local system user creation
class myazureadoauthenticator(LocalAzureAdOAuthenticator):
      def normalize_username(self, username):
          print('DEBUG>>>>> inside normalize_username()...: ' , str(username))
          return username.lower().split('@')[0]

c.JupyterHub.authenticator_class = myazureadoauthenticator

c.Application.log_level = 'DEBUG'

#### AZURE CONFIG ####

#The Azure Active Directory Tenant ID
c.AzureAdOAuthenticator.tenant_id = '7b042726-e047-4c99-ad85-2a964c859efe'
c.AzureAdOAuthenticator.client_id = 'b2f1b6fb-c156-443d-9855-71ab3b039837'
c.AzureAdOAuthenticator.client_secret = '.Lc8Q~8b_jBM~itIE9nZIVMpTG3TInpYJHuyNc3c'

#Callback URL to use
c.AzureAdOAuthenticator.oauth_callback_url = 'https://zage.ksz.ch:8888/hub/oauth_callback'


#### IP & SSL ####

c.JupyterHub.hub_ip = '127.0.0.1'

#enabling ssl for jupyterhub
c.JupyterHub.ssl_key = '/etc/letsencrypt/live/zage.ksz.ch/privkey.pem'
c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/zage.ksz.ch/fullchain.pem'


#### User management ####

#if False, the login doesn't start automatically, but with a “Login with…” link at /hub/login
c.AzureAdOAuthenticator.auto_login = False

#Use LocalAuthenticator to create system users
c.LocalAzureAdOAuthenticator.create_system_users = True

#Delete any users from the database that do not pass validation
c.AzureAdOAuthenticator.delete_invalid_users = False

#The field in the userdata response from which to get the JupyterHub username (email, username,...)
c.AzureAdOAuthenticator.username_claim = 'unique_name'

#adding users: 
c.LocalAzureAdOAuthenticator.add_user_cmd = ['adduser', '-q', '-gecos', '""', '--disabled-password']


####
from subprocess import check_call

def pre_spawn_hook(spawner):
    username = spawner.user.name        
    try:
        check_call(['useradd','-ms', '/bin/bash', username])
    except Exception as e:
        print(f'{e}')
c.Spawner.pre_spawn_hook = pre_spawn_hook
####

######### inside jupyter #########

#Set of users with admin rights
c.JupyterHub.admin_users = { 'kava', 'service-admin'}
#c.AzureAdOAuthenticator.admin_users = {'kava'}

#Set of usernames that are not allowed to log in
#c.AzureAdOAuthenticator.blocked_users = {'zagetest'}

c.JupyterHub.api_tokens = { 'e16b82417a951f9c25d40da1f04979a43277d1ae6e635cae57acb8f6ef697003':'kava' }
c.JupyterHub.api_tokens = { '6cc93427bfcf4309b08da5ae704c0cc3' : 'mopf'}

#important for api
c.JupyterHub.services = [
    {
        # give the token a name
        "name": "service-admin",
        "api_token": "046a32adcfcdad2df5ccdebb2a9e07c23fba4a4076e42def22ffe24bcf3729a6",
        # "admin": True, # if using JupyterHub 1.x
    },
    {
        # give the token a name
        "name": "kava",
        "api_token": "e16b82417a951f9c25d40da1f04979a43277d1ae6e635cae57acb8f6ef697003",
        # "admin": True, # if using JupyterHub 1.x
    },
    {
        # give the token a name
        "name": "mopf",
        "api_token": "6cc93427bfcf4309b08da5ae704c0cc3",
        # "admin": True, # if using JupyterHub 1.x
         },

]

# roles were introduced in JupyterHub 2.0
# prior to 2.0, only "admin": True or False was available

c.JupyterHub.load_roles = [
    {
        "name": "service-admin",
        "scopes": [
            # specify the permissions the token should have
            "admin:users",
            "admin:servers",
            "read:hub",
            "read:users",
            "list:users",
        ],
        "services": [
            # assign the service the above permissions
            "service-admin",
        ],
    }
]


