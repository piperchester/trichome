__author__ = 'piperchester'

import argparse


def config():
    parser = argparse.ArgumentParser(description='Fuzz test a web-based application.')
    parser.add_argument('discover', metavar='discover', type=str, nargs='+', help='list all discovered inputs of target')
    parser.add_argument('test', metavar='test', type=str, nargs='+',
                        help='discovers all inputs, then exploits inputs')
    args = parser.parse_args()

if __name__ == 'config':
    config()
