import os
import argparse

from main import init, add_user, add_card, delete_card

parser = argparse.ArgumentParser()

parser.add_argument('--init',
                    metavar='directory',
                    action = 'store',
                    help = 'Инициализация')

subparsers = parser.add_subparsers()
add_card_parser = subparsers.add_parser('add_card',
                                        help = 'Добавить карточку')
add_card_parser.add_argument('card_name',
                                action='store',
                                help='Название карточки')
add_card_parser.add_argument('question_path',
                                action='store',
                                help='Путь к файлу с вопросом')
add_card_parser.add_argument('answer_path',
                                action='store',
                                help='Путь к файлу с ответом')

parser.add_argument('--delete_card',
                    metavar='card_name',
                    help = 'Удалить карточку')

args = parser.parse_args()

# Инициализация
if args.init:
    directory = args.init
    status, message = init(directory)
    print(message)
    if status:
        username = os.getlogin()
        print(add_user(username))

# Добавление карточки
args_vars = vars(args)
if 'card_name' in args_vars.keys() and \
    'question_path' in args_vars.keys() and \
    'answer_path' in args_vars.keys():
    username = os.getlogin()
    status, message = add_card(
		            username,
		            args_vars['card_name'],
		            args_vars['question_path'],
		            args_vars['answer_path'])
    print(message)

# Удаление карточки
if args.delete_card:
    card_name = args.delete_card
    username = os.getlogin()
    status, message = delete_card(username, card_name)
    print(message)
