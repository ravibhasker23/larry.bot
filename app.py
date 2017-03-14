#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "larry.bot":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    projectLoc = parameters.get("searchLoc")
    experience = parameters.get("number")
    designation = parameters.get("searchdesignation")
    technology = parameters.get("searchTech")  

    resource = {'JAVA':10, '.Net':2, 'HTML':3, 'Blue Prism':4, 'Open Source':5}
    exp = {1:'One', 2: 'Two', 3:'Three'}
    
    speech = "The number of " + technology + " resources available are " + str(resource[technology]) + " at " + projectLoc 
    #speech = speech1 + " at " + projectLoc + " having experience of " + str(exp[experience]) + " years "
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "larry.bot"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
