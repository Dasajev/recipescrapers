 # -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from bs4 import BeautifulSoup
import requests
import re
import json

def getUrl(url, nocache=False, params=None, headers=None, cookies=None):
	"""Gets data, bs and headers for the given url, using the internal cache if necessary"""

	browser = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
	# Common session for all requests
	s = requests.session()
	s.verify = False
	s.stream = True  # Don't fetch content unless asked
	s.headers.update({'User-Agent': browser})
	# Custom headers from requester
	if headers:
	    s.headers.update(headers)
	# Custom cookies from requester
	if cookies:
	    s.cookies.update(cookies)

	try:
	    r = s.get(url, params=params)
	except requests.exceptions.InvalidSchema:
	    log.error("Invalid schema in URI: %s" % url)
	    return None
	except requests.exceptions.ConnectionError:
	    log.error("Connection error when connecting to %s" % url)
	    return None

	size = int(r.headers.get('Content-Length', 0)) // 1024
	#log.debug("Content-Length: %dkB" % size)
	if size > 2048:
	    log.warn("Content too large, will not fetch: %skB %s" % (size, url))
	    return None

	return r

def scrape(url):
	r = getUrl(url)
	bs = BeautifulSoup(r.content)
	if not bs:
		return

	recipe={}

	title_header = bs.find("h2", {'class': "recipe-title"})
	name = title_header.find("span").get_text()
	recipe["name"]=name
	
	ingredients = []
	names = bs.findAll("span", {'itemprop': "name"})
	amounts = bs.findAll("span", {'itemprop': "amount"})
	#skip recipe name 
	names = names[1:]
	for idx, name in enumerate(names):
		ingredient = {}
		ingredient["amount"] = amounts[idx].get_text()
		ingredient["name"] = name.get_text()
		ingredients.append(ingredient)
		print (ingredient)

	div = bs.find("div", {'itemprop':"instructions"})
	instructions = div.get_text().strip()

	
	recipe["instructions"]=instructions
	recipe["ingredients"]=ingredients
	print (json.dumps(recipe))


if __name__ == '__main__':
	url = u"http://thepioneerwoman.com/cooking/2014/02/chicken-mozzarella-pasta/"
	scrape(url)