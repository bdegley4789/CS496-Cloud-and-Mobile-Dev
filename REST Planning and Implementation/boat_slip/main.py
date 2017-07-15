from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty()
    length = ndb.IntegerProperty()
    at_sea = ndb.BooleanProperty()

#Boat Handler Start
class BoatHandler(webapp2.RequestHandler):
    def post(id):
        boat_data = json.loads(id.request.body)
        new_boat = Boat(name=boat_data['name'])
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['id'] = new_boat.key.urlsafe()
        id.response.write(json.dumps(boat_dict))

    #View specific boat
    def get(id, name=None):
        if name:
            b = ndb.Key(urlsafe=name).get()
            b.at_sea = True
            b.put()
            b_d = b.to_dict()
            b_d['id'] = name
            id.response.write(json.dumps(b_d))

    #Put boat in at sea or in docking area
    def put(id, name=None):
        if name:
            b = ndb.Key(urlsafe=name).get()
            boat_data = json.loads(id.request.body)
            new_boat = boat_data['at_sea']
            b.at_sea = new_boat
            b.put()
            b_d = b.to_dict()
            b_d['id'] = name
            id.response.write(json.dumps(b_d))

    #Delete boat
    def delete(id, name=None):
        if name:
            b = ndb.Key(urlsafe=name).delete()

#Boat Handler End

class Slip(ndb.Model):
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty()
    arrival_date = ndb.StringProperty()

#Slip Handler Start
class SlipHandler(webapp2.RequestHandler):
    def post(id):
        slip_data = json.loads(id.request.body)
        new_slip = Slip(number=slip_data['number'])
        new_slip.put()
        slip_dict = new_slip.to_dict()
        slip_dict['id'] = new_slip.key.urlsafe()
        id.response.write(json.dumps(slip_dict))
    
    def get(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).get()
            s_d = s.to_dict()
            s_d['id'] = number
            id.response.write(json.dumps(s_d))

    #Put boat id in current boat
    def put(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).get()
            slip_data = json.loads(id.request.body)
                #if (s.current_boat != null):
                #raise ValueError(403)
            new_slip = slip_data['current_boat']
            new_date = slip_data['arrival_date']
            s.current_boat = new_slip
            s.arrival_date = new_date
            s.put()
            s_d = s.to_dict()
            s_d['id'] = number
            id.response.write(json.dumps(s_d))

    #Delete Slip
    def delete(id, number=None):
        if number:
            s = ndb.Key(urlsafe=number).delete()

#Slip Handler End

# [START main_page]
class MainPage(webapp2.RequestHandler):
    
    def get(id):
        id.response.write("Welcome to boats and slips by Bryce Egley")
# [END main_page]
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/boat', BoatHandler ),
                               ('/boat/(.*)', BoatHandler),
                               ('/slip', SlipHandler ),
                               ('/slip/(.*)', SlipHandler),
                               ], debug=True)
# [END app]
