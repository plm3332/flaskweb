from flask_login import UserMixin
from db_model.mysql import conn_mysqldb

class User(UserMixin):
    def __init__(self, user_id, user_name, user_password):
        self.id = user_id
        self.user_name = user_name
        self.user_password = user_password
    
    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE ID = '" + str(user_id) + "' "
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], user_name=user[1], user_password=user[2])
        return user
    
    @staticmethod
    def find(user_name, user_password):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE NAME = '%s' and PASSWORD = '%s'" % (user_name, user_password)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        
        user = User(user[0], user[1], user[2])
        return user
    
    @staticmethod
    def create(user_name, user_password):
        user = User.find(user_name, user_password)
        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info(name, password) VALUES('%s', '%s')" % (str(user_name), str(user_password))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_name)
        else:
            return user