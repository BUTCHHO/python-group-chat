import socket
import pickle
from database_execute_system import *
import sqlite3



# with sqlite3.connect('database.db') as DBconnection:
#     cursor = DBconnection.cursor()
#     print(type(cursor))
#     create_table(cursor,'posts')
#     create_table(cursor, 'accounts')
#     cursor.close()
#     DBconnection.commit()


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5011))
server.listen(3)
run_server = True
print('сервер запущен')
while run_server:
    clientConnection, clientAddress = server.accept()
    print('connected: ' , clientAddress)
    clientRequest = pickle.loads(clientConnection.recv(1024))

    if clientRequest['request_type'] == "REQUEST_MESSAGES":
        with sqlite3.connect('database.db') as DBconnection:
            cursor = DBconnection.cursor()
            posts = get_messages(cursor)
            cursor.close()
            clientConnection.send(pickle.dumps(posts))

    elif clientRequest['request_type'] == "REQUEST_CREATE_ACCOUNT":
        with sqlite3.connect('database.db') as DBconnection:
            cursor = DBconnection.cursor()
            create_account(cursor,{"name":clientRequest["name"],"password":clientRequest["password"]})

    elif clientRequest['request_type'] == "REQUEST_LOGIN_ACCOUNT":
        with sqlite3.connect('database.db') as DBconnection:
            cursor = DBconnection.cursor()
            logged = login_account(cursor,clientRequest) #вернет кортеж (bool, user_id)) или (bool,) если не вошел в акк
            print(f'login_account result {logged} строчка 43')
            if logged[0]:
                clientConnection.send(pickle.dumps({'logged': logged[0], 'id':logged[1][0]}))
            else:
                clientConnection.send(pickle.dumps({'logged': logged}))
            del logged

    elif clientRequest["request_type"] == 'REQUEST_LOG_OUT':
        with sqlite3.connect('database.db') as DBconnection:
            cursor = DBconnection.cursor()
            logout(cursor,clientRequest)
    elif clientRequest['request_type'] == "REQUEST_POST_MESSAGE":
        with sqlite3.connect('database.db') as DBconnection:
            cursor = DBconnection.cursor()
            isLogged = is_logged(cursor,clientRequest['id']) #возвращает (None,), ('true',), ('false',)
            print(f'is logged result {isLogged} строка 58')
            if isLogged[0] == 'true':
                write_message(cursor,clientRequest)
            else:
                print('user not logged. Message request denied')


    clientConnection.close()

