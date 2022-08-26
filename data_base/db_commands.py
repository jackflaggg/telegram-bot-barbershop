import sqlite3


class Database:
    def __init__(self, path_to_db="salon.db"):
        self.path_to_db = path_to_db

    # Подключение к дб
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=True):
        if not parameters:
            parameters = tuple()
        data = None
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    # Создаем таблицу клиентов
    def create_table_clients(self):
        sql = """
        CREATE TABLE Clients(
        userid int NOT NULL,
        username varchar(255) NULL,
        name varchar(255) NOT NULL,
        phone varchar(255) NULL,
        longitude float NULL,
        latitude float NULL,
        time_ varchar(255) NULL,
        service int NULL,
        weekday_index int NULL,
        PRIMARY KEY (userid)
        );
        """
        self.execute(sql, commit=True)

    def update_user(self,userid: int,service_id:int, weekday_index, time):
        sql = "UPDATE Clients SET service = ? , weekday_index = ? , time_ = ? WHERE userid = ?"
        parameters = (service_id, weekday_index, time, userid)
        return self.execute(sql, parameters=parameters, fetchone=True)


    def add_user(self, userid: int, username: str, name: str):
        sql = "INSERT INTO Clients (userid, username, name) VALUES (?,?,?)"
        parameters = (userid, username, name)
        self.execute(sql, parameters=parameters, commit=True)


    def select_user(self, userid: int):
        sql = "SELECT * FROM Clients WHERE userid = ?"
        parameters = (userid,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_all_users(self):
        sql = "SELECT * FROM Clients"
        return self.execute(sql, fetchall=True)

    def save_location(self, userid: int, long, lat):
        sql = "UPDATE Clients SET longitude = ? , latitude = ? WHERE userid = ?"
        parameters = (long, lat, userid)
        return self.execute(sql, parameters=parameters, fetchone=True)


    def update_number(self, userid: int, number):
        sql = "UPDATE Clients SET phone = ?  WHERE userid = ?"
        parameters = (number, userid)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def reset_user_zapis(self, userid: int):
        sql = "UPDATE Clients SET time_ = ? , weekday_index = ?, service = ? WHERE userid = ?"
        parameters = (None, None, None, userid)
        return self.execute(sql, parameters=parameters, fetchone=True)

    # Создаем таблицу барберов
    def create_table_barbers(self):
        sql = """
        CREATE TABLE Barbers(
        id INTEGER PRIMARY KEY,
        photo_id varchar(255) NOT NULL,
        name varchar(255) NOT NULL,
        phone varchar(255) NULL,
        longitude float NULL,
        latitude float NULL,
        opisaniya int NULL,
        url	TEXT NULL
        );
        """
        self.execute(sql, commit=True)

    def add_barber(self, photo_id: str, name: str, phone: str, longitude: float, latitude: float, opisaniya:str):
        sql = "INSERT INTO Barbers (photo_id, name, phone, longitude, latitude, opisaniya) VALUES (?,?,?,?,?,?)"
        parameters = (photo_id, name, phone, longitude, latitude, opisaniya)
        self.execute(sql, parameters=parameters, commit=True)

    def get_all_barbers(self):
        sql = "SELECT * FROM Barbers"
        return self.execute(sql, fetchall=True)

    def get_barber(self, barber_id):
        sql = "SELECT * FROM Barbers WHERE id = ?"
        parameters = (barber_id,)
        return self.execute(sql,parameters=parameters, fetchone=True)

    def delete_barber(self, barber_id:int):
        sql = "DELETE FROM Barbers WHERE id = ?"
        parameters = (barber_id,)
        self.execute(sql, parameters=parameters)

    # Создаем таблицу услуги
    def create_table_uslugi(self):
        sql = """
        CREATE TABLE Services(
        id INTEGER PRIMARY KEY,
        owner int,
        description TEXT NOT NULL,
        price float NULL
        );
        """
        self.execute(sql, commit=True)

    def add_service(self, owner, description, price):
        sql = "INSERT INTO Services (owner, description, price) VALUES (?, ?, ?)"
        parameters = (owner, description, price)
        self.execute(sql, parameters=parameters, commit=True)

    def get_all_services(self, barber_id):
        sql = "SELECT * FROM Services WHERE owner = ?"
        parameters = (barber_id,)
        return self.execute(sql,parameters=parameters, fetchall=True)

    def get_service(self, service_id):
        sql = "SELECT * FROM Services WHERE id = ?"
        parameters = (service_id,)
        return self.execute(sql,parameters=parameters, fetchone=True)

    def delete_service(self, service_id):
        sql = "DELETE FROM Services WHERE id = ?"
        parameters = (service_id,)
        return self.execute(sql,parameters=parameters)