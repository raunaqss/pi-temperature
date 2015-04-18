import datetime
import logging
import string
import sys

from google.appengine.ext import db
from google.appengine.api import memcache

def temp_key(date):
    return db.Key.from_path('temp', date.strftime('%c'))


def date_midnight(d):
	"""d: date object"""
	return datetime.datetime.combine(d, datetime.time(0))


def get_date(reading, n):
	if reading:
		return date_midnight(reading.timestamp.date()) - datetime.timedelta(
			days = n)