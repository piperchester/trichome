#!/bin/env/python3

import sys, urllib, re, requests
import parser
from crawler.crawler import Crawler, Gatherer

from bs4 import BeautifulSoup

if sys.version_info < (3,0):
	print('Uh oh. Trichome requires Python 3.')
	sys.exit(1)


def validate_protocol(url):
	"""Checks URL for HTTP..."""
	target = ''.join(url)
	if 'http://' not in target:
		target = 'http://' + target
	return target

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
	print(urlParameters)
	return urlParameters;

def get_url_parameters(link):
	if(link != None):
		url = urllib.parse.urlparse(link)
		parameters = urllib.parse.parse_qs(url.query)
		return parameters.keys()
	return []	
			

def submit(response, link):	
	"""Attempt POSTs based on the query string."""
	target = response.url + link['href']
	target = re.sub('[\?q\=]', '', target)
	payload = {}

	with requests.Session() as s:
		s.post(target, data=payload)
		r = s.get(target)

def report(inputs=''):
	"""Writes found inputs to a text file."""

	# TODO(team): decide if we want to go this route

	with open('inputs.txt', 'w+') as f:
		f.write('{: ^50}\n\n'.format('System Inputs'))

		f.write('{:-^50}\n'.format('Input Fields'))
		for i in inputs:
			f.write('Alt: {0} Name: {1}\n'.format(i['alt'], i['name']))
		f.close()

def discover(url):
	"""Retrieves information from the provided URL."""
	print("Beginning...")
	c = Crawler()
	g = Gatherer()
	result = c.crawl(url[0], g)
	print("FINISHED CRAWLING")
	print(result)

def command_line_runner():
	"""Consumes commands to trichome."""
	command_parser = parser.get_parser()
	args = vars(command_parser.parse_args())

	if args['discover']:
		target = args['URL']
		result = discover(target)

if __name__ == "__main__":
	command_line_runner()