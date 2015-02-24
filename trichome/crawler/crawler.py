import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_absolute(url):
	return bool(urlparse(url).netloc)

def filter_rest(filter_lambda, interable):
	filtered = []
	rest = []
	for i in interable: 
		if filter_lambda(i):
			filtered.append(i)
		else:
			rest.append(i)
	return (filtered, rest)


class Gatherer(object):
	"""docstring for Gatherer"""
	def __init__(self):
		super(Gatherer, self).__init__()
		
	def did_hit_url(self, url, body):
		print("Hit -> " + url)

class Crawler(object):
	"""docstring for Crawler"""
	def __init__(self, url, debug=False, auth=False):
		super(Crawler, self).__init__()
		self.session = requests.session()
		self.debug = debug
		self.url = url
		
		if(auth):
			authPostData = {'username' : 'admin', 'password' : 'password', 'Login' : 'Login'}
			self.session.post(url, data=authPostData)

	def crawl(self, gathers):
		self.bfs(self.url, self.url, [], gathers)

	def log(self, msg):
		if self.debug:
			print("[BFS CRAWLER]:" + msg)

	def bfs(self, url_base, url, visited, gathers):
		self.log("Starting BFS link Crawler on " + url)
		# Do the BFS
		visited.append(url)
		main = self.session.get(url, verify=False)
		if("text/html" in main.headers['content-type'].split(';')):

			# Public to Gathesr
			for g in gathers:
				g.did_hit_url(url, main.content)

			# Parse the DOM
			htmltree = BeautifulSoup(main.content)
			(linkTags, rest) = filter_rest(lambda x: 'href' in x.attrs, htmltree.findAll('a'))
			
			# Show debug info for refless a tags
			for d in rest:
				self.log("No followable href on " + str(d)) 

			# Map the href tag
			links = list(map(lambda x: x.attrs['href'], linkTags))

			# Check for base origin, aka
			#   se.rit.edu/whatever <- has origin
			#   /whatever <- does not have origin
			(has_origin, root_origin) = filter_rest(is_absolute, links)

			# Filter out the links that leave the origin
			origin = urlparse(url_base)
			(same_origin, leaf) = filter_rest(lambda x: urlparse(x).netloc == origin.netloc, has_origin)

			# Debug logging
			for l in leaf:
				self.log("Url leaves origin " + l)

			# Make all the links from origin
			followable = same_origin + list(map(lambda x: origin.scheme + '://' + origin.netloc + x, root_origin))

			# Follow links recursivly that you haven't been too
			all_visited = []
			for l in [i for i in followable if i not in visited]:
				all_visited.append(self.bfs(url_base, l, visited, gathers))

			# When done return visited, not really used with the gathersers
			return all_visited
		else:
			self.log("None parseable content type for " + url + " -> " + main.headers['content-type'])
