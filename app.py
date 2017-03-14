from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello world1'
    
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery()
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    res = json.dumps(res, ensure_ascii=False).encode('utf8')
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def makeYqlQuery():
    return "select * from html where url=\"http://eva.vn/bep-eva-c162.html\" and xpath =\"//*[@id='centerContent']/div[2]/div[1]/div[1]/h2/a\""


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}
    
    result = query.get('results')
    if result is None:
        return {}

    a = result.get('a')
    if a is None:
        return {}
    speech = "Today you can try: " + a.get('content')

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "food-suggest"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host='0.0.0.0')
