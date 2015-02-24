#!/bin/env/python3

import sys, urllib, re, requests
import parser
from crawler.crawler import Crawler, Gatherer

from bs4 import BeautifulSoup

if sys.version_info < (3,0):
	print('Uh oh. Trichome requires Python 3.')
	sys.exit(1)


def get_inputs(response):
	"""Finds input fields on page."""
	soup = BeautifulSoup(response.text)
	inputs = soup.find_all('input')
	return inputs

def get_links(response):
	"""Find links on page, add to crawls tuple."""
	soup = BeautifulSoup(response.text)
	tags = soup.find_all('a')
	links = []
	for tag in tags:
		links.append(tag.get('href'))
	return links

def get_query_strings(links):
	"""Find all query strings from links dict."""
	urlParameters = {}
	for link in links:
		urlParameters[link] = get_url_parameters(link);
	return urlParameters;

def get_url_parameters(link):
	if link:
		url = urllib.parse.urlparse(link)
		parameters = urllib.parse.parse_qs(url.query)
		return parameters.keys()
	return []

def get_cookies(response):
	"""Returns a dict of cookies from the given response."""
	if response:
		return requests.utils.dict_from_cookiejar(response.cookies)

def report(inputs=None, links=None, cookies=None):
	"""Writes found inputs to a text file."""
	with open('input_report.txt', 'w+') as f:
		f.write('{: ^50}\n\n'.format('System Inputs'))
		f.write('{:-^50}\n'.format('Input Fields'))
		if inputs:
			for i in inputs:
				f.write('Alt: {0} Name: {1}\n'.format(i['alt'], i['name']))
		f.write('{:-^50}\n'.format('Reachable Links'))
		if links:
			for link in links:
				f.write(link.join('\n'))
		f.write('{:-^50}\n'.format('Cookies'))			
		if cookies:
			for cookie in cookies:
				f.write('{0} : {1}\n'.format(cookie, cookies[cookie]))
		f.close()

def discover(url, common_words=None):
	"""Retrieves information from the provided URL."""
	print("Beginning...")
	c = Crawler(url[0], auth=True)
	g = Gatherer()

	class Test(Gatherer):
		"""docstring for Test"""
		def __init__(self):
			super(Test, self).__init__()
			self.count = 0
			
		def did_hit_url(self, url, body):
			# Not gonna call super, super just logs
			self.count = self.count + 1
			print(self.count)

	# result = c.crawl([Test(), Gatherer()])
	print("FINISHED CRAWLING")
	r = requests.get(url[0])
	inputs = get_inputs(r)
	
	# TODO(michael): pass the result of the crawl back to our reporter
	cookies = get_cookies(r)
	report(inputs, None, cookies)

def get_common_words(words_file):
	"""Converts words from text file into list."""
	words = []
	with open(words_file.name, 'r') as f:
		words.append(f.read().strip())
	f.closed
	return words

def command_line_runner():
	"""Consumes commands to trichome."""
	command_parser = parser.get_parser()
	args = vars(command_parser.parse_args())

	if args['discover']:
		target = args['URL']
		words = []
		if args['common_words']:
			words_file = args['common_words'][0]
			words = get_common_words(words_file)

		result = discover(target, words)

if __name__ == "__main__":
	command_line_runner()