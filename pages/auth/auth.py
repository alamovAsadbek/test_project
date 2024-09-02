import hashlib
import threading

from components.random_password.generate_password import generate_password
from components.random_username.generate_username import get_username
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
        USERNAME VARCHAR(255) NOT NULL UNIQUE,
        PASSWORD VARCHAR(255) NOT NULL,
        IS_LOGIN BOOLEAN DEFAULT FALSE,
        CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def create_test_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tests (
        ID BIGSERIAL PRIMARY KEY,
        USER_ID BIGINT REFERENCES users(ID) NOT NULL,
        NAME VARCHAR(255) NOT NULL,
        TEST_ID BIGINT NOT NULL,
        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        STATUS VARCHAR(255) NOT NULL DEFAULT 'Active'
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def create_question_table(self):
        self.create_test_table()
        query = '''
        CREATE TABLE IF NOT EXISTS questions (
        ID SERIAL PRIMARY KEY,
        TEST_ID BIGINT REFERENCES tests(ID) NOT NULL,
        NAME VARCHAR(255) NOT NULL,
        CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def create_option_table(self):
        self.create_question_table()
        query = '''
        CREATE TABLE IF NOT EXISTS options (
        ID SERIAL PRIMARY KEY,
        QUESTION_ID BIGINT REFERENCES questions(ID),
        NAME VARCHAR(255) NOT NULL,
        IS_TRUE BOOLEAN DEFAULT FALSE,
        CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def create_answers_table(self):
        self.create_test_table()
        query = '''
        CREATE TABLE IF NOT EXISTS answers (
        ID SERIAL PRIMARY KEY,
        USER_ID BIGINT REFERENCES users(ID) NOT NULL,
        TEST_ID BIGINT REFERENCES tests(ID) NOT NULL,
        CORRECT_ANSWERS BIGINT NOT NULL,
        WRONG_ANSWERS BIGINT NOT NULL,
        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def create_answer_items_table(self):
        self.create_answers_table()
        query = '''
        CREATE TABLE IF NOT EXISTS answer_items (
        ID SERIAL PRIMARY KEY,
        USER_ID BIGINT REFERENCES users(ID) NOT NULL,
        QUESTION_ID BIGINT REFERENCES questions(ID),
        IS_TRUE BOOLEAN DEFAULT FALSE,
        ANSWER_ID BIGINT REFERENCES answers(ID),
        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        execute_query(query)
        return True

    @log_decorator
    def login(self):
        username: str = input("Enter your username: ").strip()
        password: str = hashlib.sha256(input("Enter your password: ").strip().encode('utf-8')).hexdigest()
        query = '''
        SELECT * FROM users WHERE USERNAME = %s AND PASSWORD = %s
        '''
        params = (username, password,)
        result_get = execute_query(query, params, fetch='one')
        if result_get is None:
            print("Invalid username or password!")
            return False
        query = '''
        UPDATE users SET IS_LOGIN = TRUE WHERE ID=%s;
        '''
        params = (result_get['id'],)
        threading.Thread(target=execute_query, args=(query, params)).start()
        print("Login successful!")
        return True

    @log_decorator
    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.__str__().encode('utf-8'))
        return hashed_password.hexdigest()

    @log_decorator
    def register(self):
        first_name: str = input("First Name: ").strip()
        last_name: str = input("Last Name: ").strip()
        print("Your account is being created...")
        username = get_username(name=first_name)
        password = generate_password()
        hash_password = self.hash_password(password)
        print(f"\nYour username: {username}\nYour password: {password}")
        query = '''
        INSERT INTO users (FIRST_NAME, LAST_NAME, USERNAME, PASSWORD) 
        VALUES (%s, %s, %s, %s);
        '''
        params = (first_name, last_name, username, hash_password)
        threading.Thread(target=execute_query, args=(query, params)).start()
        print("Register successfully")
        return True

    @log_decorator
    def logout(self):
        self.create_user_table()
        threading.Thread(target=self.create_test_table).start()
        threading.Thread(target=self.create_question_table).start()
        threading.Thread(target=self.create_option_table).start()
        threading.Thread(target=self.create_answers_table).start()
        threading.Thread(target=self.create_answer_items_table).start()
        query = '''UPDATE users SET IS_LOGIN=FALSE;'''
        execute_query(query)
        return True
