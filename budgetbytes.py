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

	title_header = bs.find("h1", {'class': "entry-title"})
	name = title_header.get_text()
	recipe["name"]=name
	
	ingredients = []
	ingredient_list = bs.findAll("li", {'itemprop': "ingredients"})
	for item in ingredient_list:
		ingredient = {}
		name = item.get_text().strip()
		dollar_pos = name.find("$")
		if dollar_pos != -1:
			name = name[:dollar_pos-1]
		ingredient["name"] = name
		ingredients.append(ingredient)

	instructions = []
	instructions_list = bs.findAll("li", {'itemprop':"recipeInstructions"})
	for item in instructions_list:
		instructions.append(item.get_text())
	
	recipe["instructions"]="".join(instructions)
	recipe["ingredients"]=ingredients
	return json.dumps(recipe)