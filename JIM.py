import json
import time
import dbserver
from log_config import log


class Server:  # прием сообщений от клиента
    @log
    def receive(r):
        a = {}
        for i in r:
            try:
                data = i.recv(1024).decode('ascii')
                if data:
                    a[i] = json.loads(data)
            except:
                pass
        return a

    @log
    def send(w, data, clients):  # обработка сообщений от клиента
        for key, value in data.items():
            if value["action"] == "get_contacts":
                Server.sendcontacts(key, value)
            if value["action"] == "authenticate":
                Server.auth(key, value)
            if value["action"] == "msg" and value["to"] == "all":
                Server.msg(key, value, clients)
            if value["action"] == "msg" and value["to"] != "all":
                clients = Server.msgto(value, clients)
            if value["action"] == "quit":
                clients = Server.quit(key, value, clients)
            if value["action"] == "add_contact":
                Server.add_contact(key, value)
            if value["action"] == "del_contact":
                Server.del_contact(key, value)
        return data, clients

    @log
    def auth(r, data):  # авторизация
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        dbserver.DbStore.login(r, t)
        user = data["user"]
        dbserver.DbStore.client(user["account_name"], r)

    @log
    def quit(r, data, clients):  # завершение работы
        message = json.dumps({"response": 200, "alert": "OK"})
        resp = message.encode('ascii')
        r.send(resp)
        clients.remove(r)
        return clients

    @log
    def msg(r, data, clients):  # отправка свободного сообщения всем клиентам
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        dbserver.DbStore.history(data, t)
        message = json.dumps(data)
        resp = message.encode('ascii')
        for i in clients:
            try:
                i.send(resp)
            except:
                pass

    @log
    def msgto(data, clients):  # Отправка персонального сообщения
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

        dbserver.DbStore.history(data, t)
        message = json.dumps(data)
        resp = message.encode('ascii')

        user = dbserver.DbStore.get_ip(data["to"])

        for i in clients:
            if str(i) == user:
                try:
                    i.send(resp)
                except:
                    clients.remove(i)
        return clients

    @log
    def sendcontacts(r, data):  # Оотправка контактов клиенту
        client_list = dbserver.DbStore.get_clients()
        quantity_clients = len(client_list)
        message = json.dumps({"response": 202, "quantity": quantity_clients})
        resp = message.encode('ascii')
        r.send(resp)
        for j in range(quantity_clients):
            time.sleep(0.001)
            message = json.dumps({"action": "contact_list", "user_id": client_list[j]})
            resp = message.encode('ascii')
            r.send(resp)

    @log
    def add_contact(r, data):  # Обработка добавления контакта
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        user = dbserver.DbStore.get_login(r)
        dbserver.DbStore.add_contact(user, data["user_id"])

    @log
    def del_contact(r, data):  # Обработка удаления контакта
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        user = dbserver.DbStore.get_login(r)
        dbserver.DbStore.del_contact(user, data["user_id"])


class Client:

    def __init__(self, name, pasw, s):
        self.name = name
        self.pasw = pasw
        self.s = s

    @log
    def auth(self):  # Pапрос авторизации
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        message = json.dumps(
            {"action": "authenticate", "time": t, "user": {"account_name": self.name, "password": self.pasw}})
        resp = message.encode('ascii')
        self.s.send(resp)

    @log
    def getcontacts(self):  # Запрос на получение контактов
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        message = json.dumps({"action": "get_contacts", "time": t})
        resp = message.encode('ascii')
        self.s.send(resp)

    @log
    def allcontacts(self, a):  # Получение котнактов
        q = a["quantity"]
        server_client_list = []
        for i in range(q):
            try:
                data = self.s.recv(1024).decode('ascii')
                n = json.loads(data)
                server_client_list.append(n["user_id"])
            except:
                pass
        return server_client_list

    @log
    def msg(self, who, data):  # Запрос на отправку простого сообщения
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        message = json.dumps(
            {"action": "msg", "time": t, "to": "all", "from": self.name, "encoding": "ascii", "message": data})
        resp = message.encode('ascii')
        self.s.send(resp)

    def quit(self):  # Запрос на выход
        message = json.dumps({"action": "quit"})
        resp = message.encode('ascii')
        self.s.send(resp)

    @log
    def addcontact(self, login):  # запрос на удаление контакта на сервере
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        message = json.dumps({"action": "add_contact", "user_id": login, "time": t})
        resp = message.encode('ascii')
        self.s.send(resp)

    @log
    def delcontact(self, login):  # запрос на добавление контакта
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        message = json.dumps({"action": "del_contact", "user_id": login, "time": t})
        resp = message.encode('ascii')
        self.s.send(resp)

    @log
    def sendto(self, who, data):  # запрос отправки персонального сообщения
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        message = json.dumps({"action": "msg", "time": t, "to": who, "from": self.name, "encoding": "ascii", "message": data})
        resp = message.encode('ascii')
        self.s.send(resp)
