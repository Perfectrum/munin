import os
import shutil
from glob import glob
import configparser
import sqlite3

# Служебная функция для получение id пользователя по его имени (логину)
def get_user_id(user_name, cursor):
    #main_connection = sqlite3.connect("main.db")
    #main_cursor = main_connection.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_name = \""+ str(user_name) +"\"")
    ids = cursor.fetchall()
    if ids == []:
        out = "There is no user with this name"
    else:
        out = ids[0][0]
    #main_connection.close()
    return(out)

###############################################################
# Функция, создающая файловую структуру в заданной директори, #
#                        запускается при первом использовании #
###############################################################
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
        
        # Создаем базу данных пользователей и карточек
        main_connection = sqlite3.connect('{}/main.db'.format(directory))
        main_cursor = main_connection.cursor()
        # Таблица с карточками в БД
        main_cursor.execute("""CREATE TABLE IF NOT EXISTS cards
                  (user_id INTEGER NOT NULL,
                   card_id INTEGER NOT NULL PRIMARY KEY, 
                   card_name TEXT NOT NULL, 
                   question TEXT NOT NULL, 
                   answer TEXT NOT NULL)""")  
        main_connection.commit()
         # Таблица с пользователями и id в БД
        main_cursor.execute("""CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER NOT NULL PRIMARY KEY,
                   user_name TEXT NOT NULL)""")  
        main_connection.commit()
        main_connection.close()

    # Запоминаем изменения в конфиге
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    return status, message


##########################################################
# Функция, добавляющая пользователя в файловую структуру #
##########################################################
def add_user(username):

    config = configparser.ConfigParser()
    config.read('config.ini')
    main_dir = config['main']['main_directory']

    # добавить пользователя в БД тут
    main_connection = sqlite3.connect('{}/main.db'.format(main_dir))
    main_cursor = main_connection.cursor()
    main_cursor.execute("SELECT * FROM users WHERE user_name = \""+ str(username) + "\"")
    if main_cursor.fetchall() == []:
        main_cursor.execute("SELECT user_id FROM users")
        idmax = main_cursor.fetchall()
        if idmax == []:
            cur_id = 1
        else:
            cur_id = max(idmax)[0]+1
        main_cursor.execute("INSERT INTO users (user_id, user_name) VALUES ("+
                            str(cur_id)+",\""+str(username)+"\")")
        main_connection.commit()
        main_connection.close()
    else:
        main_connection.close()
        print("User with this name already exists")
        return "User with this name already exists"

    # Создаем папку с карточками
    os.mkdir('{}/{}'.format(main_dir, username))

    return 'Добавлен пользователь {}'.format(username)


##############################################
# Функция, добавляющая пользователю карточку #
##############################################
def add_card(username, card_name, question_path, answer_path, additional_files_paths=[]):

    config = configparser.ConfigParser()
    config.read('config.ini')
    main_dir = config['main']['main_directory']

    # Если карточка с таким названием уже есть, отказ
    if False: # вот тут проверка существования карточки в БД
        status = False
        message = 'A card with this name alreday exists'
    # Если карточки с таким названием нет, пытаемся ее добавить
    else:
        message = ''
        status = True

        # Если какой-то из путей не валидный, отказ
        files_paths = additional_files_paths
        files_paths.append(question_path)
        files_paths.append(answer_path)

    # Подключаемся к БД
    main_connection = sqlite3.connect('{}/main.db'.format(main_dir))
    main_cursor = main_connection.cursor()

    # Проверяем существование карточки в БД
    user_id = get_user_id(username, main_cursor)
    main_cursor.execute("SELECT * FROM cards WHERE card_name =\""+
                        str(card_name) +"\" AND user_id = " + str(user_id))
    # Если карточки нет в БД, пробуем ее создать
    if main_cursor.fetchall() == []:
   
        # Проверяем существование файлов
        for file_path in files_paths:
            if os.path.exists(file_path):
                 message+= 'File {} is OK\n'.format(file_path)
            else:
                message+= 'File {} does not exist\n'.format(file_path)
                status = False
		
        # Если с путями все в порядке, их надо добавить в нужные директории
        if status:
		    # Проверяем, в правильной ли директории лежат файлы
            for file_path in files_paths:
                cur_right_path = '{}/{}/{}'.format(main_dir, username, card_name)
		        # Если файл лежит правильно, не трогаем его
                if file_path[:file_path.rindex('/')] == cur_right_path:
                    message+= 'File {} in the right folder\n'.format(file_path)
                else:
                    # Если файл лежит неправильно, копируем куда надо
                    if not os.path.exists(cur_right_path): os.mkdir(cur_right_path)
                    shutil.copyfile(file_path, '{}/{}'.format(
		                                                    cur_right_path,
		                                                    file_path.split('/')[-1]))
                    message+= 'File {} in the wrong folder. Copied to {}\n'.format(
		                                        file_path, cur_right_path)
            # Добавляем карточку в БД
            main_cursor.execute("SELECT card_id FROM cards")
            idmax = main_cursor.fetchall()
            if idmax == []:
            	cur_id = 1
            else:
            	cur_id = max(idmax)[0]+1
            main_cursor.execute("INSERT INTO cards (user_id, card_id, card_name, question, answer) VALUES ("+
                                str(user_id)+","+
				str(cur_id)+",\""+
				str(card_name)+"\",\""+
				str(question)+"\",\""+
				str(answer)+"\")")
            main_connection.commit()
        else:
            status = False
            message+= 'Card {} is already exists'.format(crad_name)	
        
    main_connection.close()

    if status:
        message+= 'Card {} is added to the user {}'.format(card_name, username)

    return status, message


###############################
# Функция, удаляющая карточку #
###############################
def delete_card(username, card_name):
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    main_dir = config['main']['main_directory']

    #  Подключаемся к БД
    main_connection = sqlite3.connect('{}/main.db'.format(main_dir))
    main_cursor = main_connection.cursor()
	
    # Если такой карточки нет, отказ
    
    user_id = get_user_id(username, main_cursor)
	
    main_cursor.execute("SELECT * FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
    if main_cursor.fetchall() == []:
        status = False
        message = 'Card {} does not exist'.format(card_name)
    # Если такая карточка существует, удаляем ее
    else:
        main_cursor.execute("SELECT card_id FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
        delid = main_cursor.fetchall()[0][0]
        main_cursor.execute("DELETE FROM cards WHERE card_name = \""+ str(card_name) +"\" AND user_id = " + str(user_id))
        main_cursor.execute("UPDATE cards SET card_id = card_id - 1 WHERE card_id > "+str(delid))
        main_connection.commit()
        status = True
    main_connection.close()


    path = '{}/{}/{}'.format(main_dir, username, card_name)
    # Если карточка существует, удаляем ее
    if os.path.exists(path):
        shutil.rmtree(path)
        status = True
        message = 'Card {} is deleted'.format(card_name)
    # Если такой карточки нет, отказ
    else:
        status = False
        message = 'Card {} does not exist'.format(card_name)
    
    return status, message

# Удаление пользователя из БД
def delete_user(user_name):
    main_connection = sqlite3.connect("main.db")
    main_cursor = main_connection.cursor()
    main_cursor.execute("SELECT * FROM users WHERE user_name = \""+ str(user_name) +"\"")
    if main_cursor.fetchall() == []:
        print("There is no user with this name")
        main_connection.close()
        return "There is no user with this name"
    else:
        main_cursor.execute("SELECT user_id FROM users WHERE user_name = \""+ str(user_name) +"\"")
        delid = main_cursor.fetchall()[0][0]
        main_cursor.execute("DELETE FROM users WHERE user_name = \""+ str(user_name) +"\"")
        main_cursor.execute("UPDATE users SET user_id = user_id - 1 WHERE user_id > "+str(delid))
        main_connection.commit()
        main_connection.close()

