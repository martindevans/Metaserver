#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class IpHandler(webapp.RequestHandler):
    def get(self):
	self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(str(self.request.remote_addr))

class NatPinHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "django/natpin.html")
	html = template.render(path, { "port" : self.request.get('port') })

	return html.decode("utf-8")

def main():
    application = webapp.WSGIApplication([('/', MainHandler),('/whatismyip', IpHandler),('/natpin*', NatPinHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
