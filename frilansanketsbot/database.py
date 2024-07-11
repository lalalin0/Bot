import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_us(self, id, katn, katd, lanr, lana, time):
        with self.connection:
            self.cursor.execute("INSERT INTO `users` VALUES (?, ?, ?, ?, ?, ?)",
                                (id, katn, katd, lanr, lana, time))
            self.connection.commit()

    def user_exist(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = self.cursor.fetchone()
        return True if user else False

    def get_users(self):
        self.cursor.execute("SELECT id FROM users")
        result = self.cursor.fetchall()
        return [value[0] for value in result]

    def select_ints(self, user_id, inter):
        self.cursor.execute("SELECT " + str(inter) + " FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def updateint(self, intg, n, user_id):
        self.cursor.execute("UPDATE users SET " + intg + " = ? WHERE id = ?", (n, user_id))
        self.connection.commit()

    def select_kats(self, user_id):
        new_list = []
        kategorieslist = ["neiro", "design"]
        for i in kategorieslist:
            self.cursor.execute("SELECT " + i + " FROM users WHERE id = ?", (user_id,))
            result = self.cursor.fetchone()
            if result and result[0] == "✅":
                new_list.append(i)
        return new_list

    def add_keyword(self, category, word):
        self.cursor.execute('INSERT INTO keywords (category, word) VALUES (?, ?)', (category, word))
        self.connection.commit()

    def delete_keyword(self, word):
        self.cursor.execute('DELETE FROM keywords WHERE word = ?', (word,))
        self.connection.commit()

    def get_keywords(self, category):
        self.cursor.execute('SELECT word FROM keywords WHERE category = ?', (category,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_keywords(self):
        self.cursor.execute('SELECT category, word FROM keywords')
        return self.cursor.fetchall()

    def get_users_ru(self):
        self.cursor.execute("SELECT id FROM users WHERE russian = ?", ("✅",))
        result = self.cursor.fetchall()
        return [value[0] for value in result]

    def get_users_en(self):
        self.cursor.execute("SELECT id FROM users WHERE american = ?", ("✅",))
        result = self.cursor.fetchall()
        return [value[0] for value in result]

    def get_exchange_status(self, user_id):
        self.cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        if self.connection:
            self.connection.close()
