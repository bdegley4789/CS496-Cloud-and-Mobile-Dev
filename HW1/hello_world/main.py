# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import datetime
#Time function is from stack overflow tutorial on time in Google App Engine
#URL: https://stackoverflow.com/questions/17908994/how-to-get-current-uk-time-in-google-app-engine

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Bryce Egley CS 496 ')
        self.response.write('This is the current time: ')
        self.response.write(datetime.datetime.now())


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
