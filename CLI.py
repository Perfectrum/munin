import os
import argparse

from main import init, add_user, add_card, delete_card, 

parser = argparse.ArgumentParser()

parser.add_argument('--init',
                    metavar='directory',
                    action = 'store',
                    help = 'Инициализация')

parser.add_argument('--add_card',
                    action='append',
                    nargs = 3,
                    metavar=('card_name', 'question_path', 'answer_path'),
                    help = 'Добавить карточку')


parser.add_argument('--delete_card',
                    metavar='card_name',
                    help = 'Удалить карточку')

parser.add_argument('--learn_cards',
                    metavar='cards_list',
                    help = 'Повторение карточек.\
                            Передается список имен карточек через запятую без пробелов.')

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
if args.add_card:
    username = os.getlogin()
    card_name = args.add_card[0][0]
    question_path = args.add_card[0][1]
    answer_path = args.add_card[0][2]
    status, message = add_card(username, card_name, question_path, answer_path)
    print(message)

# Удаление карточки
if args.delete_card:
    card_name = args.delete_card
    username = os.getlogin()
    status, message = delete_card(username, card_name)
    print(message)

# Повторение карточек
if args.learn_cards:
    for card_name in args.learn_cards.split(',')):
        question_path, answer_path = get_card(card_name)
        print('Вопрос карточки')        
        os.startfile(question_path)
        input('Enter чтобы показать ответ')
        os.startfile(answer_path)

        result = None
        while result != 0 and result != 1:
            feedback = input('Cчитать эту карточку изученной? [y/n]')

            if an.lower() in ['y', 'yes', 'true']:
                result = 1
            elif result.lower() in ['n', 'no', 'false']:
                result = 0
        
        # Записать в БД событие recall
