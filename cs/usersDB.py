import pymysql


class Database:

    def __init__(self):
        pass

    def get_connection(self):
        conn = pymysql.connect(host="localhost", user="team12", passwd="pandapanda", db="team12_wego")
        return conn

    def insert_user(self, email, name, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        print("cursos is created")
        query = "INSERT INTO users(Email,Name,Password) VALUES('%s', '%s', '%s');"
        query = query % (
            email, name, password)
        print(query)
        cursor.execute(query)
        connection.commit()
        print("User created successfully")
        connection.close()

    def user_alreadyexits(self, email, name, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "SELECT Email from users where Email='%s';"
        query = query % (email)
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        try:
            if len(rows) == 0:
                self.insert_user(email, name, password)
            else:
                return 1
        except Exception as error:
            return error
        connection.close()

    def authenticate(self, email, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "SELECT Email, Password from users where Email='%s' and Password='%s';"
        query = query % (email, password)
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        try:
            if (rows[0][0] == email) and (rows[0][1] == password):
                return 1
            else:
                return 0
        except Exception as error:
            return error
        connection.close()
