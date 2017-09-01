from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from webapp2_extras import sessions
import logging
import webapp2
import json
import subprocess
import string
import webbrowser
import urllib
import urllib2
import random
from string import Template

class OauthHandler(webapp2.RequestHandler):
    def get(self):
        logging.debug('The contents of the GET request are: ' + repr(self.request.GET))
        state = self.request.get('state')
        code = self.request.get('code')
        self.response.write("Google Plus Account Info")
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        self.response.write("Page Description: We have used the authorization token to get your basic account info and displayed it below")
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        try:
            post_data = {'code':code,'client_id':'769721252673-j7tjc6dttcu2rvkqhbch6gkrjpm1559m.apps.googleusercontent.com','client_secret':'_rLltMaY6zAFyi-WjevYPgYF','redirect_uri':'https://oauth2-174402.appspot.com/oauth','grant_type':'authorization_code'}
            form_data = urllib.urlencode(post_data)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            post_response = urlfetch.fetch(url='https://www.googleapis.com/oauth2/v4/token',payload=form_data,method=urlfetch.POST,headers=headers)
            #self.response.write(post_response.content)
        except urlfetch.Error:
            logging.exception('Caught exception fetching post url')
        jsonData = json.loads(post_response.content)
        token = jsonData["access_token"]
        #self.response.write(token)
        try:
            tokenFinal = "Bearer " + token
            get_data = {}
            head = {'Authorization':tokenFinal}
            get_response = urlfetch.fetch(url='https://www.googleapis.com/plus/v1/people/me',payload=get_data,method=urlfetch.GET,headers=head)
            #self.response.write(get_response.content)
            jsonData2 = json.loads(get_response.content)
            temp1 = jsonData2["name"]
            url = jsonData2["url"]
            first = temp1["givenName"]
            last = temp1["familyName"]
            self.response.write("First Name: ")
            self.response.write(first)
            self.response.write("""<html><he><bod><br /></bod></he></html>""")
            self.response.write("Last Name: ")
            self.response.write(last)
            self.response.write("""<html><he><bod><br /></bod></he></html>""")
            self.response.write("Google Plus: ")
            self.response.write(url)
            self.response.write("""<html><he><bod><br /></bod></he></html>""")
        except urlfetch.Error:
            logging.exception('Caught exception fetching get url')
        self.response.write("State Variable: ")
        self.response.write(state)

# [START main_page]
class MainPage(webapp2.RequestHandler):
    
    def get(self):
        self.response.write("OAuth 2.0 by Bryce Egley")
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        self.response.write("Description: This website will test oauth 2.0 by requesting a token to authorize this website to view your Google Plus first and last name.")
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        self.response.write("Authorize Google Plus account info---->")
        state = ''.join(random.choice(string.lowercase) for i in range(15))
        htmlUrl = ("""
    <html>
    <head><title>Submit</title></head>
    <body>
    <a href='https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=769721252673-j7tjc6dttcu2rvkqhbch6gkrjpm1559m.apps.googleusercontent.com&redirect_uri=https://oauth2-174402.appspot.com/oauth&scope=email&state=$state'>Submit</a>
    </body></html>
    """)
        self.response.write(Template(htmlUrl).safe_substitute(state=state))

# [END main_page]

# [START app]
app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/oauth', OauthHandler )
                               ], debug=True)
# [END app]
