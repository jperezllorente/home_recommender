import json, requests

def extract(url):

    '''

    This function allows us to extract the information of the Foursquare API so that we can work with it. (It can be
    ised with other APIs) Once the information has been extracted, it is treated so that we can work with the
    dictionary elements form the JSON object. The only argument required is the url that needs to be filled with the
    corresponding parameters that can beo found in the developer manual.

    '''

    results = requests.get(url)

    code = json.loads(results.text)

    decoding = code.get("response")

    decoded = decoding.get("groups")[0]

    return decoded.get("items")