'''
Module Name: test_web_crawler.py
Author: "Raman Monga"
Email: "mongaraman@gmail.com"
Purpose: Test class for Sainsbury web page crawler.
Description: This module contains code for unit testing for Sainsbury web crawl.
Date: 16th Feb 2016
'''

import unittest
import requests
from bs4 import BeautifulSoup
from web_crawler import WebCrawler

class TestWebCrawler(unittest.TestCase):
	''' Test class for Sainsbury Crawler. '''

	def setUp(self):
		''' Initial setup method.'''

		self.main_pg_url = 'http://hiring-tests.s3-website-eu-west-1.amazonaws'\
			'.com/2015_Developer_Scrape/5_products.html'
		self.prd_pg_url = 'http://hiring-tests.s3-website-eu-west-1.' \
			'amazonaws.com/2015_Developer_Scrape/sainsburys-apricot-' \
			'ripe---ready-320g.html'
		self.crawl_obj = WebCrawler()
		self.prod_page_html = BeautifulSoup('<div class='\
			'"productTitleDescriptionContainer"><h1>Sainsbury\'s Apricot Ripe' \
			' & Ready x5</h1></div><div class="pricing"><p class=' \
			'"pricePerUnit">&pound;3.50</p></div><div class="productText">' \
			'<p>Apricots</p></div>', 'lxml')
		self.main_page_html = BeautifulSoup('<div class="productInfo"><a' \
			' href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/' \
			'2015_Developer_Scrape/sainsburys-apricot-ripe---ready-320g.html"' \
			'>Sainsbury\'s Apricot Ripe &amp; Ready x5</a>' \
			'<div class="productTitleDescriptionContainer"><h1>Sainsbury\'s' \
			' Apricot Ripe & Ready x5</h1></div><p class="pricePerUnit">' \
			'&pound;3.50<span class="pricePerUnitUnit">unit</span></p>' \
			'<div class="productText">Apricots</div></div>' \
			'<div class="productInfo"><a ' \
			'href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/' \
			'2015_Developer_Scrape/sainsburys-avocado-xl-pinkerton-loose-' \
			'300g.html">Sainsbury\'s Avocado Ripe &amp; Ready XL Loose 300g' \
			'</a><div class="productTitleDescriptionContainer"><h1>' \
			'Sainsbury\'s Avocado Ripe & Ready XL Loose 300g</h1></div>' \
			'<p class="pricePerUnit">&pound;1.50<span class="pricePerUnitUnit"'\
			'>unit</span></p><div class="productText">Avocados</div></div>',
		'lxml')

		self.dummy_pg_url = 'http://hiring-tests.s3-website-eu-west-1.amazonaws'\
			'.com/2015_Developer_Scrape/dummy_products.html'

	def test_get_page_request_object(self):
		'''Validate get page request method. it should return response object.
		'''
		# Validate main product page
		req_obj = self.crawl_obj.get_page_request_object(self.main_pg_url)
		assert req_obj is not None
		self.assertEqual(req_obj.status_code, 200)
		self.assertEqual(req_obj.url, self.main_pg_url)
		
		# Validate child product page
		req_obj = self.crawl_obj.get_page_request_object(self.prd_pg_url)
		assert req_obj is not None
		self.assertEqual(req_obj.status_code, 200)
		self.assertEqual(req_obj.url, self.prd_pg_url)

	def test_get_products_urls(self):
		''' test product urls from webpage '''

		# mock html extracted using beautifulsoup library
		def beautifulsoup_html_mock(param1, param2):
			return self.main_page_html
		import web_crawler
		web_crawler.BeautifulSoup = beautifulsoup_html_mock
		prd_link = self.crawl_obj.get_products_urls(self.main_pg_url)
		self.assertEqual(len(prd_link), 2)
	
		prd_link = self.crawl_obj.get_products_urls(self.dummy_pg_url)
		self.assertEqual(len(prd_link), 0) # if there are not products

	def test_get_page_contents(self):
		''' test one of the product page contents '''
		
		# mock html extracted using beautifulsoup library
		def beautifulsoup_html_mock(param1, param2):
			return self.prod_page_html

		import web_crawler
		web_crawler.BeautifulSoup = beautifulsoup_html_mock
		self.crawl_obj.get_page_contents(self.prd_pg_url)
		final_dict = self.crawl_obj.final_dict
		self.assertEqual(len(final_dict), 2)
		self.assertEqual(final_dict.get('total'), 3.5)
		self.assertEqual(final_dict['result'][0].get('description'), 'Apricots')
		self.assertEqual(final_dict['result'][0].get('unit_price'), 3.5)
		self.assertEqual(final_dict['result'][0].get('title'), 'Sainsbury\'s' \
			' Apricot Ripe & Ready x5')

	def test_crawl_page(self):
		
		# mock html extracted using beautifulsoup library
		def beautifulsoup_html_mock(param1, param2):
			return self.main_page_html
		
		import web_crawler
		web_crawler.BeautifulSoup = beautifulsoup_html_mock
		
		prd_link = self.crawl_obj.get_products_urls(self.main_pg_url)
		self.assertEqual(len(prd_link), 2)

		self.crawl_obj.crawl_page(self.main_pg_url)
		final_dict = self.crawl_obj.final_dict
		self.assertEqual(len(final_dict), 2)
		
		self.assertEqual(final_dict.get('total'), 7)
		self.assertEqual(final_dict['result'][0].get('description'), 'Apricots')
		self.assertEqual(final_dict['result'][0].get('unit_price'), 3.5)
		self.assertEqual(final_dict['result'][0].get('title'), 'Sainsbury\'s' \
			' Apricot Ripe & Ready x5')
		

