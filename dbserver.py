import sqlite3


class DbStore():
    @staticmethod
    def create_db():
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS client(client_id TEXT,'
                    'info TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS history_login(time TEXT,'
                    'ip TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS contacts(owner_id TEXT,'
                    'client_id TEXT)')

        cur.execute('CREATE TABLE IF NOT EXISTS history_client(client_id TEXT,'
                    'time TEXT,'
                    'message TEXT)')
        cur.close()
        con.close()

    def login(ip, time):
        data = [str(time), str(ip)]
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('INSERT INTO history_login VALUES (?,?)', data)
        con.commit()
        cur.close()
        con.close()

    def client(login, ip):  # Запись в БД логин и IP клиента
        data = [login, str(ip)]
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM client WHERE client_id = "' + login + '"')
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO client VALUES (?,?)', data)
            con.commit()
        else:
            cur.execute('UPDATE client SET client_id = "' + login + '", info = "' + str(
                ip) + '" WHERE client_id ="' + login + '"')
            con.commit()
        cur.close()
        con.close()

    @staticmethod
    def get_clients():
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        clients = []
        try:
            cur.execute('SELECT client_id FROM client')
            result = cur.fetchall()
            for i in result:
                clients.append(i[0])
            con.commit()
        except:
            pass

        cur.close()
        con.close()
        return clients

    def history(data, time):
        data = [data["from"], time, data["message"]]
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO history_client VALUES (?,?,?)', data)
            con.commit()
        except:
            pass
        cur.close()
        con.close()

    def get_login(ip):  # поиск клиента по IP
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM client WHERE info = "' + str(ip) + '"')
        result = cur.fetchone()
        cur.close()
        con.close()
        return result[0]

    def get_ip(login):  # поиск клиента по IP
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('SELECT info FROM client WHERE client_id = "' + str(login) + '"')
        result = cur.fetchone()
        cur.close()
        con.close()
        return result[0]

    def add_contact(owner, login):  # поиск клиента по IP
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM contacts WHERE client_id = "' + login + '" and owner_id ="' + owner + '"')
        result = cur.fetchone()
        data = [owner, login]
        if result is None:
            cur.execute('INSERT INTO contacts VALUES (?,?)', data)
            con.commit()
        else:
            pass
        cur.close()
        con.close()

    def del_contact(owner, login):  # поиск клиента по IP
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute('SELECT client_id FROM contacts WHERE client_id = "' + login + '" and owner_id ="' + owner + '"')
        result = cur.fetchone()
        if result is None:
            pass
        else:
            cur.execute('DELETE FROM contacts WHERE client_id = "' + login + '" and owner_id ="' + owner + '"')
            con.commit()
        cur.close()
        con.close()
