import datetime
import logging
import string

from google.appengine.ext import db
from google.appengine.api import memcache

from utils import *


class Temperature(db.Model):
	"""Datastore entitiy for each temperature reading."""

	celsius = db.FloatProperty(required = True)
	fahrenheit = db.FloatProperty(required = True)
	timestamp = db.DateTimeProperty(required = True)

	@classmethod
	def construct(cls, cel, fah, ts):
		return cls(parent = temp_key(ts.date()),
				   celsius = cel,
				   fahrenheit = fah,
				   timestamp = ts)

	

