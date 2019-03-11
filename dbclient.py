import sqlite3


class DbStore():
    def __init__(self, name):
        self.name = name

    def create_db(self):
        con = sqlite3.connect(str(self.name) + '.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS history_message(client_id INTEGER,'
                    'time TEXT,'
                    'message TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS contacts(client_id TEXT PRIMARY KEY)')
        cur.close()
        con.close()

    def add_client(self, login):
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

    def del_client(self, login):

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

    def show_client(self):

        con = sqlite3.connect(self.name + '.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM contacts')

        result = cur.fetchall()
        nicklist = [i[0] for i in result]
        return nicklist
        cur.close()
        con.close()
