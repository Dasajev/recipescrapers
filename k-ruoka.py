 # -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from bs4 import BeautifulSoup
import requests
import re
import json
import utils

def scrape(url):
	r = utils.getUrl(url)
	bs = BeautifulSoup(r.content)
	if not bs:
		return

	recipe={}

	title = bs.find("h2", {'class': "header-theme-color"})
	name = title.get_text()
	recipe["name"]=name
	
	ingredients = []
	for row in bs.findAll("dl", {'itemprop': "ingredients"}):
		amounts = []
		names = []
		for dts in row.findAll("dt"):
			amount_unit = dts.get_text().strip()
			amounts.append(amount_unit)
		for dds in row.findAll("dd"):
			name = dds.find("span", {'class':"ingredient-text"}).get_text().strip()
			names.append(name)

		for idx, name in enumerate(names):
			ingredient = {}
			ingredient["amount"] = amounts[idx]
			ingredient["name"] = name
			ingredients.append(ingredient)

	instructions = []
	ul = bs.find("ul", {'itemprop':"recipeInstructions"})
	for li in ul.findAll("li"):
		instructions.append(li.findAll("span")[1].get_text())

	recipe["instructions"]="".join(instructions)
	recipe["ingredients"]=ingredients
	print (json.dumps(recipe))


if __name__ == '__main__':
	url = u"http://www.k-ruoka.fi/reseptit/valimeren-kasvispiirakka"
	scrape(url)
