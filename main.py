import os
from glob import glob
import configparser
import sqlite3

###############################################################
# Функция, создающая файловую структуру в заданной директори, #
#                        запускается при первом использовании #
###############################################################


# Запись карт очки в БД
def insert_card(user_id, card_name, question, answer):
    main_connection = sqlite3.connect("main.db")
    main_cursor = main_connection.cursor()
    main_cursor.execute("SELECT * FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
    if main_cursor.fetchall() == []:
        main_cursor.execute("SELECT card_id FROM cards")
        cards_data = [(user_id, card_name, question, answer)]        
        main_cursor.execute("INSERT INTO cards (user_id, card_name, question, answer) VALUES ("+
                            str(user_id)+",\""+str(card_name)+"\",\""+str(question)+"\",\""+str(answer)+"\")")
        main_connection.commit()
        main_connection.close()
    else:
        main_connection.close()
        print("Card with this name already exists")
        return "Card with this name already exists"


# Удаление карт очки из БД
def delete_card(user_id, card_name):
    main_connection = sqlite3.connect("main.db")
    main_cursor = main_connection.cursor()
    main_cursor.execute("SELECT * FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
    if main_cursor.fetchall() == []:
        print("There is no card with this name")
        main_connection.close()
        return "There is no card with this name"
    else:
        main_cursor.execute("SELECT card_id FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
        delid = main_cursor.fetchall()[0][0]
        main_cursor.execute("DELETE FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
        main_cursor.execute("UPDATE cards SET card_id = card_id - 1 WHERE card_id > "+str(delid))
        main_connection.commit()
        main_connection.close()


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
        # База данных
        main_connection = sqlite3.connect("main.db")
        main_cursor = main_connection.cursor()
        # Таблица с карточками в БД
        main_cursor.execute("""CREATE TABLE IF NOT EXISTS cards
                  (user_id INTEGER NOT NULL,
                   card_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                   card_name TEXT NOT NULL, 
                   question TEXT NOT NULL, 
                   answer TEXT NOT NULL)""")  
        main_connection.commit()
        # Таблица с пользователями и id в БД
        main_cursor.execute("""CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   user_name TEXT NOT NULL)""")  
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
