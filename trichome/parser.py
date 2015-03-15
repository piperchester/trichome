#!/bin/env/python3

import argparse


def get_parser():
  """Initializes the argument parser."""
  parser = argparse.ArgumentParser(description='trichome: the one-stop-shop for web-based vulnerability testing')
  parser.add_argument('discover', help=
                      'list all discovered inputs of target', nargs='?')
  parser.add_argument('test', help=
                      'discovers all inputs, then exploits inputs', nargs='?')
  parser.add_argument('URL', help=
                      'target to fuzz-test', nargs=1)
  parser.add_argument('-w', '--common-words', nargs=1, type=argparse.FileType('r'), help=
                      'newline-delimited file of common words to be used in page guessing and input guessing') 
  parser.add_argument('-a', '--customauth', help=
                      'signals that trichome should use hard-coded auth for a specific application (e.g. dvwa)')
  parser.add_argument('-v', '--vectors', nargs=1, type=argparse.FileType('r'), help=
                      'newline-delimited file of common exploits to vulnerabilities')
  parser.add_argument('-s', '--sensitive', nargs=1, type=argparse.FileType('r'), help=
                      "newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response")  
  parser.add_argument('-r', '--random', default=False, action='store_true', help=
                      "when off, try each input to each page systematically. When on, choose a random page, then a random input field and test all vectors. Default: false.")
  parser.add_argument('-z', '--slow', type=int, default=500, help=
                      "number of milliseconds considered when a response is considered 'slow'. Default is 500 milliseconds")
  return parser


