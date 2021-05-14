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
        pass # Создать БД тут
    
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
