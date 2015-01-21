#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas
import requests

from .defaults import *


class StoreRestClient(object):

	def __init__(self, host=DEFAULT_HOST):
		self.host = host

	def save(self, data, reference, symbol, jsonformat=DEFAULT_JSON_FORMAT):
		json = data.to_json(orient=jsonformat, date_format='iso')
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		url = '{host}{api_prexif}/{reference}/{symbol}?jsonformat={jsonformat}'.format(host=self.host,
			                                                                           api_prefix=API_URL_PREFIX,
			                                                                           reference=reference,
			                                                                           symbol=symbol,
			                                                                           jsonformat=jsonformat)
		response = requests.post(url, data=json, headers=headers)
		return response.status_code in [200, 201]

	def retrieve(self, reference, symbol, start=None, end=None, jsonformat=DEFAULT_JSON_FORMAT):
		url = '{host}{api_prexif}/{reference}/{symbol}?jsonformat={jsonformat}'.format(host=self.host,
			                                                                           api_prefix=API_URL_PREFIX,
			                                                                           reference=reference,
			                                                                           symbol=symbol,
			                                                                           jsonformat=jsonformat)
		if start:
			url += '&start=%s' % start.isoformat()
		if end:
			url += '&end=%s' % end.isoformat()

		response = requests.get(url)
		if response.status_code not in [200, 201]:
			return None

		json = flask.request.get_data()
		return pandas.read_json(json, orient=jsonformat)


class StoreRestDatasource(object):

    def __init__(self, reference, host=DEFAULT_HOST):
    	self.reference = reference
		self.rest_client = StoreRestClient(host)

    def evaluate(self, context, symbol, start=None, end=None):
        return self.rest_client.retrieve(self.reference, symbol, start=start, end=end)