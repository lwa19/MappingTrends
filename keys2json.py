# generate a json file with consumer and access keys (dev account: @lwa19)

import json

'''
# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = 'K9VFm4Wd16nJjYsqCjbNEl3oN'
credentials['CONSUMER_SECRET'] = 'B3dA5JQFRCXxHfKbcGJB8BR18RHRjM1LfZh5euWui66CPvKqeS'
credentials['ACCESS_TOKEN'] = '623730595-7p4tdPla1EhlULAtn71mVWHYQR0Jm3LO2HaIEZnU'
credentials['ACCESS_SECRET'] = '7bqovm47TzxXLl2e51EiFLLq8LGm0OCfqGOwNBFWA7tIS'
'''

# Enter your keys/secrets as strings in the following fields - Pooja's version
credentials = {}
credentials['CONSUMER_KEY'] = 'b366BUMXBWu8okLFh7O5O4MWG'
credentials['CONSUMER_SECRET'] = 'lADAhVdQnFAWjHEWC09TkqfoWjTUPkv9nSGZwq9dxzSGGXGEXO'
credentials['ACCESS_TOKEN'] = '1226271974072168448-a7jfrD7yQVMEgzIAE0M9mzw6DvWSFg'
credentials['ACCESS_SECRET'] = 'BRv3yWrpV5WkhFNfq8yOvu82rxzRk42eJt0Rrv9I7hGjI'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)