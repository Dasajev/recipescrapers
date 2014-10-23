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

	title_dev = bs.find("div", {'class': "title-wrapper"})
	name = title_dev.find("span").get_text()
	recipe["name"]=name
	
	ingredients = []
	table = bs.find("table", {'class': "list-ingredients"})
	for row in table.findAll("tr"):
		ingredient = {}
		cell = row.find("td", {'class': "name"})
		if cell is None:
			continue

		name = cell.find("span").renderContents().decode("utf8")

		cell = row.find("td", {'class':"amount-unit"})
		if cell is not None:
			amount = cell.find("span", {'data-view-element': "amount"}).renderContents().decode("utf8")
			unit = cell.find("span", {'data-view-element': "unit"}).renderContents().decode("utf8")

		ingredient["name"]=name
		ingredient["amount"]=amount
		ingredient["unit"]=unit
		ingredients.append(ingredient)

	div = bs.find("div", {'class':"instructions"})
	instructions = div.get_text().strip()

	recipe["instructions"]=instructions
	recipe["ingredients"]=ingredients

	return json.dumps(recipe)