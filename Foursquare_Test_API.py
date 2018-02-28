import json, requests
url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
  client_id='2HCWH445BK3EJLSLYD2KIMEINLSSBKEAHCRTT1PFYCHAXRI4',
  client_secret='ATX2IQWUCYQJRJVWC0DQT1BOBHEJ4OTL3EFWLCSX50JWDLTF',
  v='20170801',
  ll='37.392971,-122.076044',
  query='pizza',
  limit=1
)
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

print resp
print data
