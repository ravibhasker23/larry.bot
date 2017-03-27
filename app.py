#!/usr/bin/env python

import urllib
import json
import os
import MySQLdb

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

def processquery(designation):
    db = MySQLdb.connect(host="122.98.107.190",    # your host, usually localhost
                     user="POC_USER",         # your username
                     passwd="pocuser",  # your password
                     db="Informatica")
    cur = db.cursor()
    return "SELECT EMPLOYEE_NAME FROM EMPLOYEE where DESIGNATION = '" +designation+ "'"

def makeWebhookResult(req):
    if req.get("result").get("action") != "chatbot.test":
        return {}
    
    result = req.get("result")
    
    parameters = result.get("parameters")
    
    

    designation = parameters.get("role")
    if designation is None:
        return {}
    #speech = "Technology you want" + technology + " Project Location " + projectLoc + "Role " + designation
    
    projectLoc = parameters.get("location")
    if projectLoc is None:
        return {}
    #speech = "Technology you want" + technology + " Project Location " + projectLoc

    technology = parameters.get("technology") 
    if technology is None:
        return {}
    
    #speech = "Technology you want" + technology

    #resource = {'JAVA' : 10, '.Net' : 2, 'Blue Prism' : 5}
           
    speech =  processquery(designation)
    #speech  = "You have searched profiles for " + technology + " for location " + prefLoc + " with experience " + experience + " and designation " + designation
    
    #speech = "Technology you want" + technology + " Project Location " + projectLoc + "Role " + designation
    
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
