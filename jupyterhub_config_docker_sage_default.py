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

#Callback URL to use. Typically https://{host}/hub/oauth_callback
c.AzureAdOAuthenticator.oauth_callback_url = 'https://zage.ksz.ch:8888/hub/oauth_callba>

#### SSL ####


#enabling ssl for jupyterhub
c.JupyterHub.ssl_key = '/etc/letsencrypt/live/zage.ksz.ch/privkey.pem'
c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/zage.ksz.ch/fullchain.pem'


#### User management ####

#if False, the login doesn't start automatically, but with a “Login with…” link at /hub>c.AzureAdOAuthenticator.auto_login = False

#Use LocalAuthenticator to create system users
c.LocalAzureAdOAuthenticator.create_system_users = True
#Delete any users from the database that do not pass validation
c.AzureAdOAuthenticator.delete_invalid_users = False

#The field in the userdata response from which to get the JupyterHub username (email, username,...)
c.AzureAdOAuthenticator.username_claim = 'unique_name'

#adding users
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

### DockerSpawner ###

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image ='jupyter_min_nb_sage_default'

# Connect containers to this Docker network
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.extra_host_config = {'network_mode': 'bridge'}

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

## Enable debug-logging of the single-user server
c.Spawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = '127.0.0.1'


### URL ###
c.JupyterHub.hub_connect_ip = 'zage.ksz.ch'


############################################################
######### inside jupyter #########

#Set of users with admmin rights
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




