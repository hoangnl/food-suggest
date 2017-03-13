import urllib2
import urllib
import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello world'
    
@app.route('/webhook', methods=['POST'])
def webhook():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery()
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    print (yql_url)
    req = urllib2.Request(yql_url).add_header('User-Agent','Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0')
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def makeYqlQuery():
    return "select * from html where url=\"http://eva.vn/bep-eva-c162.html\" and xpath =\"//*[@id='centerContent']/div[2]/div[1]/div[1]/h2/a\""


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}
    print (query)
    
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
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host='0.0.0.0')
