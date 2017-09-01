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
#import requests
import time
from string import Template

GloPortfolios = []
GloStocks = []

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
            post_data = {'code':code,'client_id':'769721252673-j7tjc6dttcu2rvkqhbch6gkrjpm1559m.apps.googleusercontent.com','client_secret':'1xNe-46AXTWHYAqtcsyqeW0e','redirect_uri':'https://brycefinal.appspot.com/oauth','grant_type':'authorization_code'}
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
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        self.response.write("Back to home page -->")
        htmlUrl4 = ("""
                <html>
                <head><title>Submit</title></head>
                <body>
                <a href='https://brycefinal.appspot.com'>Home</a>
                </body></html>
                """)
        self.response.write(htmlUrl4)




#Stock
class Stock(ndb.Model):
    #Symbol
    symbol = ndb.StringProperty(required=True)
    #Number of stocks in Portfolio
    shares = ndb.IntegerProperty(required=True)
    #Date purchases
    date = ndb.StringProperty()
    #Starting price
    stockPrice = ndb.IntegerProperty()
    #Current value
    portfolioNumber = ndb.IntegerProperty(required=True)

#Stock Handler Start
class StockHandler(webapp2.RequestHandler):
    #Buy a new stock
    def post(id):
        #Google Stocks API
        #r = requests.get('http://finance.google.com/finance/info?client=ig&q=NASDAQ:AAPL')
        #jsonData = r.json()
        #jsonTemp = jsonData.replace('//', '');
        #jsonFin = jsonTemp[0]
        #sPrice = 192.15
        stock_data = json.loads(id.request.body)
        new_stock = Stock(symbol=stock_data['symbol'],shares=stock_data['shares'],date=time.strftime("%d/%m/%Y"),stockPrice=5,portfolioNumber=stock_data['portfolioNumber'])
        new_stock.put()
        stock_dict = new_stock.to_dict()
        stock_dict['id'] = new_stock.key.urlsafe()
        id.response.write(json.dumps(stock_dict))
        global GloStocks
        GloStocks.append(stock_dict['id'])
    
    #Get current info on id stock
    def get(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).get()
            s_d = s.to_dict()
            s_d['id'] = number
            id.response.write(json.dumps(s_d))

    #Put Stock id into portfolio
    def put(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).get()
            stock_data = json.load(id.request.body)
            new_shares = stock_data['shares']
            new_price = stock_data['stockPrice']
            s.count = new_shares
            s.value = new_price
            s.put()
            s_d = s.to_dict()
            s_d['id'] = number
            id.response.write(json.dumps(s_d))
    
    #Sell Stock
    def delete(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).delete()

#Stock Handler End


#Portfolio
class Portfolio(ndb.Model):
    #Name of portfolio
    name = ndb.StringProperty(required=True)
    #Number
    number = ndb.IntegerProperty(required=True)
    #Number of stocks in Portfolio
    count = ndb.IntegerProperty()
    #Current value
    value = ndb.IntegerProperty()

#Portfolio Handler Start
class PortfolioHandler(webapp2.RequestHandler):
    #Create a new portfolio
    def post(id):
        portfolio_data = json.loads(id.request.body)
        #User must specify name and number of portfolio
        new_portfolio = Portfolio(name=portfolio_data['name'],number=portfolio_data['number'],count=0,value=0)
        #Amount of stocks and Value of Portfolio will start at 0 and $0
        new_portfolio.put()
        portfolio_dict = new_portfolio.to_dict()
        portfolio_dict['id'] = new_portfolio.key.urlsafe()
        id.response.write(json.dumps(portfolio_dict))
        global GloPortfolios
        GloPortfolios.append(portfolio_dict['id'])
    
    #Get info on id portfolio
    def get(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).get()
            s_d = s.to_dict()
            s_d['id'] = number
            id.response.write(json.dumps(s_d))


    #Change portfolio count and value when adding new stock to portfolio
    def put(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).get()
            portfolio_data = json.load(id.request.body)
            new_count = portfolio_data['count']
            new_value = portfolio_data['value']
            s.count = new_count
            s.value = new_value
            s.put()
            s_d = s.to_dict()
            s_d['id'] = number
            id.response.write(json.dumps(s_d))

    #Delete Slip
    def delete(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).delete()

#Portfolio Handler End

#View all Portfolios
class PortfolioView(webapp2.RequestHandler):
    def get(id):
        global GloPortfolios
        #self.response.write("Copy and paste key without quotes after https://brycefinal.appspot.com/portfolio/")
        for x in range(0,len(GloPortfolios)):
            id.response.write(json.dumps(GloPortfolios[x]))


#View all Stocks
class StockView(webapp2.RequestHandler):
    def get(id):
        global GloStocks
        #self.response.write("Copy and paste key without quotes after https://brycefinal.appspot.com/stock/")
        for x in range(0,len(GloStocks)):
            id.response.write(json.dumps(GloStocks[x]))


# [START main_page]
class MainPage(webapp2.RequestHandler):
    
    def get(self):
        self.response.write("CS496 Final Project by Bryce Egley")
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        self.response.write("Description: This website allows users to sign in and create portfolios for stocks")
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        self.response.write("Authorize Google Plus account info---->")
        state = ''.join(random.choice(string.lowercase) for i in range(15))
        htmlUrl = ("""
    <html>
    <head><title>Submit</title></head>
    <body>
    <a href='https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=769721252673-j7tjc6dttcu2rvkqhbch6gkrjpm1559m.apps.googleusercontent.com&redirect_uri=https://brycefinal.appspot.com/oauth&scope=email&state=$state'>Submit</a>
    </body></html>
    """)
        self.response.write(Template(htmlUrl).safe_substitute(state=state))
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        
        #View Portfolios for app
        self.response.write("View all portfolios---->")
        htmlUrl2 = ("""
                <html>
                <head><title>Submit</title></head>
                <body>
                <a href='https://brycefinal.appspot.com/portfolioView'>View</a>
                </body></html>
                """)
        self.response.write(htmlUrl2)
        self.response.write("""<html><he><bod><br /></bod></he></html>""")
        
        #View stocks for app
        self.response.write("View all Stocks---->")
        htmlUrl3 = ("""
        <html>
        <head><title>Submit</title></head>
        <body>
        <a href='https://brycefinal.appspot.com/stockView'>View</a>
        </body></html>
        """)
        self.response.write(htmlUrl3)

# [END main_page]

# [START app]
app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/oauth', OauthHandler ),
                               ('/portfolio', PortfolioHandler ),
                               ('/portfolio/(.*)', PortfolioHandler),
                               ('/stock', StockHandler ),
                               ('/stock/(.*)', StockHandler),
                               ('/stockView', StockView),
                               ('/stockView/(.*)', StockView),
                               ('/portfolioView', PortfolioView),
                               ('/portfolioView/(.*)', PortfolioView)
                               ], debug=True)
# [END app]
