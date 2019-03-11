import socket
import json
import JIM
import dbclient
import threading
import sys



def client_receive(user, s):
    while True:
        global server_client_list
        try:
            data = s.recv(1024).decode('ascii')
            a = json.loads(data)
            try:
                if a["response"] == 202:
                    server_client_list = user.allcontacts(a)
                    for i in server_client_list:
                        print(i)
                if a["response"] == 200:
                    break
            except:
                if a["action"] == "msg":
                    print(a["from"], ': ', a["message"])
        except:
            print ("Сервер остановлен")
            break


def help():
    print("[get] - запрос перечня пользователей с сервера")
    print("[show] - вывод клиентов из списка контактов")
    print("[add] {имя контакта} - добавление пользователя в контакты")
    print("[del] {имя контакта} - удаление пользователя из контактов")
    print("[msg] {текст сообщения} - отправка сообщения всем пользователям")
    print("[help] - вызов справки")
    print("[exit] - выход")


def client_write():
    while True:
        local_client_list = user_db.show_client()
        msg = input()
        command = msg.split(" ", 1)
        if command[0] == "get":  # Команда для запроса списка клиентов с сервера
            user.getcontacts()
        elif command[0] == "add":  # Команда для добавления клиента в контакты клиента
            try:
                client_id = command[1]
                if client_id in server_client_list and client_id != name:
                    user_db.add_client(client_id)
                    user.addcontact(client_id)
                else:
                    print("Неверное имя")
            except:  # Вывод ошибки при поптыке добавить пользователя
                print('Сначала необходимо запросить список пользователей [get]')
        elif command[0] == "del":  # Команда для удаления клиента из контактов клиента
            client_id = command[1]
            if client_id in local_client_list:
                user_db.del_client(client_id)
                user.delcontact(client_id)
            else:
                print("Неверное имя")
        elif command[0] == "show":  # Просмотр списка контактов
            if local_client_list:
                for i in local_client_list:
                    print(i)
            else:
                print("Список контактов пуст")
        elif command[0] == "help":  # Вызов помощи
            help()
        elif command[0] == "exit":  # Выход
            user.quit()
            rT.join()
            break
        elif command[0] == "msg":  # Сообщение всем пользователям
            user_db.history("all", command[1])
            user.msg("all", command[1])
        elif command[0] == "sendto":  # Персональное сообщение пользователю
            msg = msg.split(" ", 2)
            if msg[1] in local_client_list:
                user_db.history(msg[1], msg[2])
                user.sendto(msg[1], msg[2])
            else:
                print("Пользователя %s нет в вашем списке" % msg[1])
        else:
            print("Нераспознанная команда")


if len(sys.argv) <= 2:
    name = "Andrey"
    pasw = "pass"
elif len(sys.argv) == 3:
    name = sys.argv[1]
    pasw = sys.argv[2]

host = 'localhost'
port = 9090
server = (host, port)
# name = "Andrey"
# pasw = "pass"
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)
    user = JIM.Client(name, pasw, s)
    user_db = dbclient.DbStore(name)
    user_db.create_db()
    user.auth()
    rT = threading.Thread(target=client_receive, args=(user, s))  # Запускаем режим приема сообщений в отдельном потоке
    rT.start()
    help()
    client_write()
    s.close()
except:
    print('Сервер не найден')
