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

class Crawler(object):
	"""docstring for Crawler"""
	def __init__(self):
		super(Crawler, self).__init__()

	def bfs(self, url_base, url, visited=[]):
		print("Starting BFS link Crawler on " + url)
		visited.append(url)
		main = requests.get(url, verify=False)
		if("text/html" in main.headers['content-type'].split(';')):
			htmltree = BeautifulSoup(main.content)
			(linkTags, rest) = filter_rest(lambda x: 'href' in x.attrs, htmltree.findAll('a'))
			# Show debug info
			for d in rest:
				print("No followable href on " + str(d)) 
			links = list(map(lambda x: x.attrs['href'], linkTags))
			(has_origin, root_origin) = filter_rest(is_absolute, links)

			origin = urlparse(url_base)
			(same_origin, leaf) = filter_rest(lambda x: urlparse(x).netloc == origin.netloc, has_origin)

			for l in leaf:
				print("Url leaves origin " + l)

			followable = same_origin + list(map(lambda x: origin.scheme + '://' + origin.netloc + x, root_origin))

			for l in [i for i in followable if i not in visited]:
				self.bfs(url_base, l, visited)
			return visited
		else:
			print("None parseable content type for " + url + " -> " + main.headers['content-type'])
