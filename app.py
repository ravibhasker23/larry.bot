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
    if req.get("result").get("action") != "chatbot.test":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    
    projectLoc = parameters.get("location")

    designation = parameters.get("role")

    technology = parameters.get("technology")  

    #resource = {'JAVA' : 10, '.Net' : 2, 'Blue Prism' : 5}
           
    #speech =  "Technology " + technology + " Project Location " + projectLoc + "Role " + designation
    #speech  = "You have searched profiles for " + technology + " for location " + prefLoc + " with experience " + experience + " and designation " + designation
    speech = technology + " reosources " + projectLoc + " " + designation 
    
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

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
