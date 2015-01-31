__author__ = 'piperchester'

import argparse


def args():
    parser = argparse.ArgumentParser(description='Fuzz test a web-based application.')
    parser.add_argument('discover', metavar='discover', type=str, nargs='+', help='list all discovered inputs of target')
    parser.add_argument('test', metavar='test', type=str, nargs='+',
                        help='discovers all inputs, then exploits inputs')
    arguments = parser.parse_args()




def main():
    print("Welcome to Fuzzer!")
    print("Please type in a command:")
    command = input()

    if command == "fuzz":
        print("fuzzing application now")


if __name__ == '__main__':
    main()
