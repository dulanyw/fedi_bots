from mastodon import Mastodon

response = Mastodon.create_app(
    'freebooksbot', #name of the app
    api_base_url = 'https://botsin.space', #address of the instance
    to_file = 'freebooksbot_clientcred.secret' #filename for storing credentials
)

print(response)
