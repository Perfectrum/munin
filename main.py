import os
from glob import glob
import configparser
import sqlite3

###############################################################
# Функция, создающая файловую структуру в заданной директори, #
#                        запускается при первом использовании #
###############################################################
# TODO: создавать БД
def init(directory):

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Если такая директория существует
    if os.path.exists(directory):
        
        # Если директория существует и пустая, ок
        if glob('{}/*'.format(directory)) == []:
            config['main']['main_directory'] = directory
            status = True
            message = 'OK, directory {} is set'.format(directory)
        # Если директория существует и не пустая, отказ
        else:
            status = False
            message = 'Directory is not empty'
    
    # Если директория не существует, создаем ее и ок
    else:
        os.mkdir(directory)
        config['main']['main_directory'] = directory
        status = True
        message = 'OK, directory {} is created and set'.format(directory)

    if status:
        # База данных с карточками
        main_connection = sqlite3.connect("main.db")
        main_cursor = main_connection.cursor()
        main_cursor.execute("""CREATE TABLE IF NOT EXISTS cards
        (user_id INT, card_id INT, card_name TEXT, question TEXT, answer TEXT)""")  
        cards_data = [(1, 1, 'eblan?', 'ty eblan?', 'da'), 
                      (2, 2, 'hui', 'how long your dick', '0'), 
                      (3, 3, 'semen', 'swallow my cum', 'yes')] 
        main_cursor.executemany("INSERT INTO cards VALUES (?,?,?,?,?)", cards_data)
        main_connection.commit()
        # База данных с пользователями и id
        main_cursor.execute("""CREATE TABLE IF NOT EXISTS users
        (user_id INT, user_name TEXT)""")  
        users_data = [(1, "XyeCoc"), 
                      (2, "Poopa"), 
                      (3, "Loopa")] 
        main_cursor.executemany("INSERT INTO users VALUES (?,?)", users_data)
        main_connection.commit()
        main_connection.close()
        # pass # Создать БД тут
    
    # Запоминаем изменения в конфиге
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    return message

##########################################################
# Функция, добавляющая пользователя в файловую структуру #
##########################################################
# TODO: добавлять пользователя в БД
def add_user(username):

    config = configparser.ConfigParser()
    config.read('config.ini')
    main_dir = config['main']['main_directory']

    # добавить пользователя в БД тут

    os.mkdir('{}/{}'.format(main_dir, username))

    return 'Добавлен пользователь {}'.format(username)


if __name__ == '__main__':
    directory = input('Введи директорию:\n')

    init_status = init(directory)
    
    print(init_status)
