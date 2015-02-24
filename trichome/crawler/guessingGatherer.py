from crawler.crawler import Gatherer
from urllib.parse import urlparse

class GuessingGatherer(Gatherer):
	def did_hit_url(self, url, body):
		fileTypes = ['php', 'jsp']
		file = open('common_words.txt', 'r')
		parsedURL = urlparse(url)
		
		
		if parsedURL.hostname != None and parsedURL.scheme != '':
			baseURL = parsedURL.scheme + '://' + parsedURL.hostname;
		
			print(baseURL)
			for line in file:
				for fileType in fileTypes:
					guessedURL = baseURL + '/' + line.rstrip() + '.' + fileType;
					print('A possible URL is: ' + guessedURL);
				