import requests
import argparse

from sys import version, exit as version, exit


if version < '3':
  print('Oh noes! Trichome require Python 3.')
  exit(1)


def discover(target, username='', password=''):
  """Retrieves information from the provided URL"""

  if 'http://' not in target:
    print("What protocol are we using? HTTP I presume?")
    target = "http://" + target

  r = requests.get(target, auth=(username, password))
  return r.json()

def get_parser():
  """Initializes the argument parser."""

  parser = argparse.ArgumentParser(description='trichome: the one-stop-shop for web-based vulnerability testing')
  parser.add_argument('discover', help=
                      'list all discovered inputs of target', nargs=1)
  parser.add_argument('test', help=
                      'discovers all inputs, then exploits inputs', nargs='?')
  parser.add_argument('-a', '--customauth', help=
                      'signals that trichome should use hard-coded auth for a specific application (e.g. dvwa)')
  parser.add_argument('-w', '--common-words', help=
                      'newline-delimited file of common words to be used in page guessing and input guessing')
  parser.add_argument('-v', '--vectors', help=
                      'newline-delimited file of common exploits to vulnerabilities')
  parser.add_argument('-s', '--sensitive', help=
                      "newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response")  
  parser.add_argument('-r', '--random', default=False, action='store_true', help=
                      "when off, try each input to each page systematically. When on, choose a random page, then a random input field and test all vectors. Default: false.")
  parser.add_argument('-z', '--slow', type=int, default=500, help=
                      "number of milliseconds considered when a response is considered 'slow'. Default is 500 milliseconds")
  return parser

def command_line_runner():
  """Consumes commands to trichome."""

  parser = get_parser()
  args = vars(parser.parse_args())

  if args['discover']:
    target = input('Enter target URL: ')
    username = input('Enter username: ')
    password = input('Enter password: ')
    print(discover(target, username, password))

if __name__ == "__main__":
  command_line_runner()