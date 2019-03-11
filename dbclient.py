import sqlite3
import time


class DbStore():
    def __init__(self, name):
        self.name = name

    def create_db(self):
        con = sqlite3.connect(str(self.name) + '.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS history_message(time TEXT,'
                    'sender TEXT,'
                    'receiver TEXT,'
                    'message TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS contacts(client_id TEXT PRIMARY KEY)')
        cur.close()
        con.close()

    def add_client(self, login):  # Добавление пользователя в БД клиента
        con = sqlite3.connect(self.name + '.db')
        cur = con.cursor()
        data = [login]
        try:
            cur.execute('INSERT INTO contacts VALUES (?)', data)
            con.commit()
            print("Пользователь %s добавлен" % login)
        except:
            print('Пользователь %s уже в списке контактов' % login)
        cur.close()
        con.close()

    def del_client(self, login):  # Удаление пользователя из БД клиента

        con = sqlite3.connect(self.name + '.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM contacts WHERE client_id ="' + str(login) + '"')
        result = cur.fetchall()
        if result:
            cur.execute('DELETE FROM contacts WHERE client_id ="' + str(login) + '"')
            con.commit()
            print("Пользователь %s удален" % login)
        else:
            print('Пользователь %s в списке не найден' % login)

        cur.close()
        con.close()

    def show_client(self):  # Выборка пользователя из списка контактов клиента

        con = sqlite3.connect(self.name + '.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM contacts')

        result = cur.fetchall()
        nicklist = [i[0] for i in result]
        return nicklist
        cur.close()
        con.close()

    def history(self, who, msg):  # Запись сообщений в БД клиента
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        con = sqlite3.connect(self.name + '.db')
        cur = con.cursor()
        data = [t, self.name, who, msg]
        cur.execute('INSERT INTO history_message VALUES (?,?,?,?)', data)
        con.commit()
        cur.close()
        con.close()
