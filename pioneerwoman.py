 # -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from bs4 import BeautifulSoup
import re
import json
import utils

def scrape(url):
	r = utils.getUrl(url)
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
		ingredient["amount"] = amounts[idx].get_text().strip()
		ingredient["name"] = name.get_text().strip()
		ingredients.append(ingredient)

	div = bs.find("div", {'itemprop':"instructions"})
	instructions = div.get_text().strip()

	
	recipe["instructions"]=instructions
	recipe["ingredients"]=ingredients
	return json.dumps(recipe)