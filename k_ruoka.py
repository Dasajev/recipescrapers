# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from bs4 import BeautifulSoup
import json
import utils


def scrape(url):
    r = utils.getUrl(url)
    bs = BeautifulSoup(r.content)
    if not bs:
        return

    recipe = {}

    j = bs.find('script', {'type': 'application/ld+json'})
    data = json.loads(j.string)
    print data

    recipe["name"] = data['description']
    recipe["instructions"] = data['recipeInstructions']
    recipe["ingredients"] = utils.split_amounts_and_ingredients(
        data['recipeIngredient']
        )
    return json.dumps(recipe)
