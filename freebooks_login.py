from mastodon import Mastodon
import os

#get the login credentials
fpt = open("freebooksbot_credentials.txt","r")
for line in fpt:
    [username,password] = line.split(",")
fpt.close()

#Login to mastodon, get API access token
mastodon = Mastodon(client_id = 'freebooksbot_clientcred.secret',)
mastodon.log_in(
    username,
    password,
    to_file = 'freebooksbot_usercred.secret'
)
