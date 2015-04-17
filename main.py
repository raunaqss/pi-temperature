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
from utils import *

# initializing jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = True)


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
		n = self.request.get('n')
		if not n:
			n = '0'
		n = int(n)
		readings = Temperature.all()
		latest_reading = readings.get()
		# For current days readings
		current = readings.ancestor(temp_key(get_date(latest_reading, n)))
		current_1 = current.get()
		if not current_1:
			self.redirect('/')
		else:
			# For the link of the older day
			older = Temperature.all().filter('timestamp <', 
				date_midnight(current_1.timestamp.date()))
			older.order('-timestamp')
			older = older.get()
			if older:
				older_diff = current_1.timestamp.date() - older.timestamp.date()
				older_n = older_diff.days
			else:
				older_n = None
			logging.error(older_n)
			# For the link of the newer day
			newer = Temperature.all().filter('timestamp >',
				date_midnight(current_1.timestamp.date()))
			newer.order('-timestamp')
			newer = newer.get()
			if newer:
				newer_diff = newer.timestamp.date() - current_1.timestamp.date(
					)
				newer_n = newer_diff.days
			else:
				newer_n = None
			logging.error(newer_n)
			self.render_template('main.html',
								 title = 'Home Temperature Monitoring System',
								 readings = current,
								 older_n = older_n,
								 newer_n = newer_n,
								 n = n)


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
