'''
Module Name: web_crawler.py
Author: "Raman Monga"
Email: "mongaraman@gmail.com"
Purpose: Sainsbury web page crawler.
Description: This module contains code for creating a console application
to consume a webpage, process some data and present it.
Date: 16th Feb 2016

Example Output json will be:
	{
		"results":[
			{
			"title":"Sainsbury's Avocado, Ripe
			"size": "90.6kb",
			"unit_price": 1.80,
			"description": "Great to eat now - avocado counts as 1 of your 5..."
			},
			{
			"title":"Sainsbury's Avocado, Ripe
			"size": "87kb",
			"unit_price": 2.00,
			"description": "Great to eat now - avocado counts as 1 of your 5..."
			}
		],
		"total": 3.80
	}

Assumptions:
1. Product urls or all products will be under object with css .productInfo
2. Product titles div will always has css as: 'productTitleDescriptionContainer'
3. unit_price will always have css as: '.pricePerUnit'
4. Prod desc will be  under element with css class as 'productText'
'''

import re
import json
import sys
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

class WebCrawler:
	''' Class used to crawl Sanisbury products list and fetch required info.'''

	def __init__(self):
		''' intialization method.
		Params:
			None
		'''

		self.final_dict = {}
		self.prod_attrs_list = []

	def get_page_request_object(self, url):
		''' Method used to get webpage request object for passed page url.
		Params:
			None
		Output:
			Returns a requests object for passed page url or None.
			Raises requests.exceptions.HTTPError as exception if status code
			is not 200.
		'''

		try:
			req_obj = requests.get(url)
			req_obj.raise_for_status()
		except HTTPError as req_err:
			return None
		return req_obj

	def get_products_urls(self, uri):
		''' Method used to return list of urls for all products on the page.
		Params:
			uri: string url
		Returns:
			list of urls
			e.g. ['http://hiring-tests.s3-website-eu-west-1.amazonaws....html',
 			'http://hiring-tests.s3-website-eu-west-1.amazonaws...html'] or []
		'''
		product_links = []
		req_obj = self.get_page_request_object(uri) #get request object of url
		if req_obj:
			xtracted_html = BeautifulSoup(req_obj.text, 'html.parser')
			product_links = xtracted_html.select('.productInfo a')
			product_links = [str(link['href']) for link in product_links]
		return product_links

	def get_page_contents(self, uri):
		''' Method used to create final dict object.
		Params:
			uri - string url of page.
		Output:
			It sets final dict variable with required output as:
			{
				"results":[
							{
							"title":"Sainsbury's Avocado, Ripe
							"size": "90.6kb",
							"unit_price": 1.80,
							"description": "Great to eat now -
							avocado counts as 1 of your 5..."
							},
							{Product 2},
							{Product 3},....
						  ],
				"total": 3.80
			}
		'''

		req_obj = self.get_page_request_object(uri) #get request object of url
		if req_obj is None:
			print "There was error in crawling web page=%s" % str(uri)

		# Extract html contents from webpage
		xtracted_html = BeautifulSoup(req_obj.text, 'html.parser')

		# Fetch required attribute values from page contents
		title = xtracted_html.select(
			'.productTitleDescriptionContainer > h1')[0].text.strip()

		unit_price = float(re.findall("\d+\.\d+", xtracted_html.select(
			'.pricePerUnit')[0].text)[0])

		desc = xtracted_html.select('.productText')[0].text.strip()

		bytes = float(req_obj.headers['content-length'])
		size = '{:.2f}kb'.format(bytes / 1024)
		
		self.prod_attrs_list.append({
			'title': title,
			'unit_price': unit_price,
			'size': size,
			'description': desc
		})
		self.final_dict["result"] = self.prod_attrs_list
		#summation of units assign it to total dict key
		self.final_dict["total"] = unit_price + self.final_dict.get(
			'total', 0)

	def crawl_page(self, page_url):
		''' Method used to crawl webpage and return prints dictionary output
		Params:
			page_url - string: web page url
		Example Output:
				{
					"results":[
								{
								"title":"Sainsbury's Avocado, Ripe
								"size": "90.6kb",
								"unit_price": 1.80,
								"description": "Great to eat now -
								avocado counts as 1 of your 5..."
								},
								{Product 2},
								{Product 3},....
							  ],
					"total": 3.80
				}
		Exit method if we cant get required resource
		'''

		# extract all products uris from page content
		product_links = self.get_products_urls(page_url)
		if len(product_links)<1:
			sys.exit("No products found on page.")

		# fetch contents from all urls and prepare required output dict
		for uri in product_links:
			self.get_page_contents(uri)

		#round off total to 3 decimal  places
		self.final_dict['total'] = round(self.final_dict.get('total', 0), 3)
		return self.final_dict

def main():
	PAGE_URL = 'http://hiring-tests.s3-website-eu-west-1.amazonaws.com/' \
               '2015_Developer_Scrape/5_products.html'

	print "Scrapping starts here............."
	crawler_obj = WebCrawler()
	products = crawler_obj.crawl_page(PAGE_URL)
	print json.dumps(products, indent=4, sort_keys=True)
	print "Scrapping ends here............."

if __name__ == '__main__':
	main()
