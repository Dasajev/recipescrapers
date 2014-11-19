import k_ruoka
import pioneerwoman
import kotikokki
import budgetbytes
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Downloads recipes as JSON.')
	parser.add_argument("url")
	args = parser.parse_args()
	
	url = args.url

	if "pioneerwoman.com" in url:
		print (pioneerwoman.scrape(url))
	elif "k-ruoka.fi" in url:
		print (k_ruoka.scrape(url))
	elif "kotikokki.net" in url:
		print (kotikokki.scrape(url))
	elif "budgetbytes.com" in url:
		print (budgetbytes.scrape(url))