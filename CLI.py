import os
import argparse

from main import init, add_user

parser = argparse.ArgumentParser()

parser.add_argument('--init',
                    metavar='directory',
                    action = 'store',
                    help = 'Инициализация')

args = parser.parse_args()

if args.init:
    directory = args.init
    print(init(directory))
    username = os.getlogin()
    print(add_user(username))
