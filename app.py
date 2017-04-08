#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
from random import randint


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
    randSource = randint(0,8)
    yql_query = makeYqlQuery(randSource)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(randSource, data)
    res = json.dumps(res, ensure_ascii=False).encode('utf8')
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def makeYqlQuery(randSource): 
    randPos = randint(1,6)
    if randSource == 0:
        query = "select * from html where url=\"http://eva.vn/bep-eva-c162.html\" and xpath =\"/html/body/div[2]/div[4]/table/tbody/tr[1]/td[2]/div/div[2]/div[1]/a\""
    elif randSource == 1:
        query = "select * from html where url=\"http://7monngonmoingay.net\" and xpath = \"/html/body/div[1]/div[2]/div[" + str(randPos) +"]/div[1]/a\""
    elif randSource == 2:
        query = "select * from html where url=\"http://www.phunutoday.vn/lam-me/\" and xpath =\"/html/body/main/div/div[1]/div[1]/div/section/div[1]/article[" + str(randPos) +"]/a"
    elif randSource == 3:
        query = "select * from html where url=\"https://naungonmoingay.com/mon-ngon/\" and xpath =\"/html/body/div[3]/div[1]/div[3]/article[" + str(randPos) +"]/div[1]/a\""
    elif randSource == 4:
        query = "select * from html where url=\"http://us.24h.com.vn/mon-ngon-moi-ngay-c460e2552.html\" and xpath = \"/html/body/div[2]/div[3]/table/tbody/tr[1]/td[2]/div/div[2]/div[" + str(randPos + 1) +"]/span[1]/a\""
    elif randSource == 5:
        query = "select * from html where url=\"http://afamily.vn/an-ngon.chn\" and xpath = \"/html/body/form/div[2]/div[4]/div[2]/div[2]/div/div[2]/div/div[" + str(randPos) +"]/a\""
    else:
        query = "select * from html where url=\"http://kenh14.vn/made-by-me/kitchen.chn\" and xpath = \"/html/body/form/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[3]/ul/li[" + str(randPos) +"]/div[1]/a\""
    return query


def makeWebhookResult(randSource, data):
    query = data.get('query')
    if query is None:
        return {}
    
    result = query.get('results')
    if result is None:
        return {}

    a = result.get('a')
    if a is None:
        return {}
    speech = a.get('title')
    
    
    if randSource == 0:
        url = "http://eva.vn/" + a.get('href')
    elif randSource == 1:
        url = a.get('href')
    elif randSource == 2:
        url = "http://www.phunutoday.vn"+ a.get('href')
    elif randSource == 3:
        url = a.get('href')
    elif randSource == 4:
        url = a.get('href')
    elif randSource == 5:
        url = "http://afamily.vn"+ a.get('href') 
    else:
        url = "http://kenh14.vn" + a.get('href')
        
    facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": a.get('title'),
                        "image_url": a.get('img').get('src'),
                        "subtitle": speech,
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": url,
                                "title": "Xem"
                            }
                        ]
                    }
                ]
            }
        }
}
    
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "data": {"facebook": facebook_message},
        "source": "food-suggest"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host='0.0.0.0')
