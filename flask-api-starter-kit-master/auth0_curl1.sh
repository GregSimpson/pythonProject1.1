curl --request POST \
  --url 'https://ttec-ped-developers.auth0.com/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=client_credentials \
  --data 'client_id=JmO3H4Y6WI3qhfe7Nu2j1ALecJ6U1nwo' \
  --data client_secret=6C23kvixcwHffFHRVktSvxS2NYJemMgxBBfj6sRIUGgqRhgVClsiBd_HCFhUf4jo \
  --data 'audience=https://ttec-ped-developers.auth0.com/api/v2/' \
  --data scope=read:roles
