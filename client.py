import socket
import json
import JIM
import dbclient
import threading


def client_receive(user, s):
    while True:
        data = s.recv(1024).decode('ascii')
        a = json.loads(data)
        global server_client_list
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
        msg = input().split(" ", 2)

        if msg[0] == "get":  # Команда для запроса списка клиентов с сервера
            user.getcontacts()
        elif msg[0] == "add":  # Команда для добавления клиента в контакты клиента
            try:
                client_id = msg[1]
                if client_id in server_client_list and client_id != name:
                    user_db.add_client(client_id)
                    user.addcontact(client_id)
                else:
                    print("Неверное имя")
            except:  # Вывод ошибки при поптыке добавить пользователя
                print('Сначала необходимо запросить список пользователей [get]')
        elif msg[0] == "del":  # Команда для удаления клиента из контактов клиента
            client_id = msg[1]
            if client_id in local_client_list:
                user_db.del_client(client_id)
                user.delcontact(client_id)
            else:
                print("Неверное имя")
        elif msg[0] == "show":  # Просмотр списка контактов
            if local_client_list:
                for i in local_client_list:
                    print(i)
            else:
                print("Список контактов пуст")

        elif msg[0] == "help":  # Вызов помощи
            help()
        elif msg[0] == "exit":  # Выход
            user.quit()
            rT.join()
            break
        elif msg[0] == "msg":  # Сообщение всем пользователям
            user.msg("all", name, msg[1])
        elif msg[0] == "sendto":  # Персональное сообщение пользователю
            if msg[1] in local_client_list:
                user.sendto(msg[1], name, msg[2])
            else:
                print("Пользователя %s нет в вашем списке" % msg[1])
        else:
            print("Нераспознанная команда")

host = 'localhost'
port = 9090
server = (host, port)
name = "Andrey"
pasw = "pass"
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
