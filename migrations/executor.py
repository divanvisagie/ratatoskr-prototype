import sqlite3

class Executor(object):
    def __init__(self):
        self.conn = sqlite3.connect("data/muninn.db")
        self.cursor = self.conn.cursor()

    def commit(self, sql, params = None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.conn.commit()


    def release_resources(self):
        self.cursor.close()
        self.conn.close()