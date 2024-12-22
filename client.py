import socket
import pickle
from user_class import User

client_run = True
user = User(None)
while client_run:
    try:
        client = socket.socket()
        client.connect(('127.0.0.1', 5011))
        client.send(pickle.dumps({"request_type": "REQUEST_MESSAGES"}))
        posts = pickle.loads(client.recv(1024))
        client.close()
        for i in posts:
            print(i)

        event = input('действие - ')

        if 'quit' in event:
            client.close()
            client_run = False

        elif 'create account' in event:
            name = input('введите имя ')
            password = input('введите пароль ')
            client = socket.socket()
            client.connect(('127.0.0.1', 5011))
            client.send(pickle.dumps({'request_type': 'REQUEST_CREATE_ACCOUNT', 'name': name, 'password': password}))
            print('аккаунт был создан (наверное)')
            client.close()

        elif 'login' in event:
            name = input('введите имя ')
            password = input('введите пароль ')
            client = socket.socket()
            client.connect(('127.0.0.1', 5011))
            client.send(pickle.dumps({"request_type": 'REQUEST_LOGIN_ACCOUNT', 'name': name, 'password': password}))
            answer = pickle.loads(client.recv(1024))
            # print(answer)
            if answer['logged'] == True:
                user.name = name
                user.logged = True
                user.id = answer['id']
                # print('id ', user.id)
            else:
                print('неверное имя или пароль ')
            client.close()

        elif 'write' in event:
            # print(user.logged)
            content = input('введите сообщение - ')
            client = socket.socket()
            client.connect(('127.0.0.1', 5011))
            client.send(pickle.dumps({"request_type": 'REQUEST_POST_MESSAGE', "author": user.name, "id": user.id, "content": content}))
            client.close()

    except KeyboardInterrupt:
        print('interrupted...')
        if user.logged:
            print('user logging out...')
            client = socket.socket()
            client.connect(('127.0.0.1',5011))
            client.send(pickle.dumps({"request_type": 'REQUEST_LOG_OUT', "id": user.id}))
            client.close()
        print('exit...')
        exit()



