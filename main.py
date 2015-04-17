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

import datetime
import jinja2
import logging
import os
import string
import time
import webapp2

from dbmodels import *

# initializing jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = True)


def temp_key(group = 'default'):
    return db.Key.from_path('temp', group)


class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render_template(self, template, **params):
		self.write(self.render_str(template, **params))


class MainHandler(Handler):

	def get(self):
	# while True:	
		readings = Temperature.all().ancestor(temp_key())
		self.render_template('main.html',
							 title = 'Home Temperature Monitoring System',
							 readings = readings)
			# time.sleep(10)


	def post(self):
		logging.error('Post request reached here.')
		cel = self.request.get('celsius')
		fah = self.request.get('fahrenheit')
		ts = self.request.get('timestamp')
		temperature = Temperature.construct(float(cel),
											float(fah),
											datetime.datetime.strptime(ts,
												'%c'))
		temperature.put()


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
