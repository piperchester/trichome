import requests
from bs4 import BeautifulSoup
from crawler.crawler import Gatherer
from urllib.parse import urlparse

class GuessingGatherer(Gatherer):
	def did_hit_url(self, url, body):
		fileTypes = ['php', 'jsp']
		file = open('common_words.txt', 'r')
		parsedURL = urlparse(url)
		
		
		if parsedURL.hostname != None and parsedURL.scheme != '':
			baseURL = parsedURL.scheme + '://' + parsedURL.hostname;
		
			# print(baseURL)
			for line in file:
				for fileType in fileTypes:
					guessedURL = baseURL + '/' + line.rstrip() + '.' + fileType;
					print('A possible URL is: ' + guessedURL);
					print('\n')

class CookieGatherer(Gatherer):
	def did_hit_url(self, url, body):
		parsedURL = urlparse(url)
		
		if parsedURL.hostname and parsedURL.scheme is not '':
			response = requests.get(url)
			cookies = requests.utils.dict_from_cookiejar(response.cookies)
			print("Possible cookies:\n")
			print(cookies)		


class CountGatherer(Gatherer):
	def __init__(self):
		super(CountGatherer, self).__init__()
		self.count = 0
		
	def did_hit_url(self, url, body):
		# Not gonna call super, super just logs
		self.count = self.count + 1
		if self.count >= 30:
			return
		else:				
			print(self.count)		

class InputGatherer(Gatherer):
	def did_hit_url(self, url, body):
		response = requests.get(url)
		soup = BeautifulSoup(response.text)
		inputs = soup.find_all('input')
		print("Possible inputs:")
		print(inputs)		
				