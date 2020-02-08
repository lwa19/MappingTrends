# generate a json file with consumer and access keys (dev account: @lwa19)

import json

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = 'K9VFm4Wd16nJjYsqCjbNEl3oN'
credentials['CONSUMER_SECRET'] = 'B3dA5JQFRCXxHfKbcGJB8BR18RHRjM1LfZh5euWui66CPvKqeS'
credentials['ACCESS_TOKEN'] = '623730595-7p4tdPla1EhlULAtn71mVWHYQR0Jm3LO2HaIEZnU'
credentials['ACCESS_SECRET'] = '7bqovm47TzxXLl2e51EiFLLq8LGm0OCfqGOwNBFWA7tIS'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)