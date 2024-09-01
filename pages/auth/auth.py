from main_files.database.db_setting import execute_query
from main_files.decorator.decorator_func import log_decorator


class Auth:
    @log_decorator
    def create_user_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
        ID SERIAL PRIMARY KEY,
        FIRST_NAME VARCHAR(255) NOT NULL,
        LAST_NAME VARCHAR(255) NOT NULL,
        USERNAME VARCHAR(255) NOT NULL,
        PASSWORD VARCHAR(255) NOT NULL,
        IS_LOGIN BOOLEAN DEFAULT FALSE,
        CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def login(self):
        pass

    @log_decorator
    def logout(self):
        self.create_user_table()
        query = '''UPDATE users SET IS_LOGIN=FALSE;'''
        execute_query(query)
        return True
