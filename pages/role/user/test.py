import threading

from components.pagination.pagination import Pagination
from components.random_password.generate_password import generate_password
from main_files.database.db_setting import get_active_user, execute_query
from main_files.decorator.decorator_func import log_decorator


class Test:
    def __init__(self):
        self.__active_user = get_active_user()
        self.__test_id = None
        self.__question_id = None

    @log_decorator
    def question_answer(self):
        is_true = False
        answer_name: str = input("Enter the answers to the questions: ")
        while True:
            print("\nIs this the correct answer?")
            print('\n1. Yes\t2. No\t\n')
            check = int(input("Choose: "))
            if check == 1:
                is_true = True
            elif check == 2:
                is_true = False
            else:
                print("Wrong input")
                continue
            print("The answer is confirmed")
            break
        query = '''
        INSERT INTO options (name, question_id, is_true) VALUES (%s, %s, %s)
        '''
        params = (answer_name, self.__question_id, is_true)
        threading.Thread(target=execute_query, args=(query, params)).start()
        return True

    @log_decorator
    def question_func(self):
        question_name: str = input("Enter your question: ")
        query = '''
        INSERT INTO questions (name, test_id) VALUES (%s, %s)
        RETURNING id
        '''
        params = (question_name, self.__test_id)
        result = execute_query(query, params, fetch='one')
        self.__question_id = result[0]
        return True

    @log_decorator
    def create_test(self):
        test_name: str = input("Enter test name: ").strip()
        number_of_questions: int = int(input("Enter number of questions: ").strip())
        number_of_answers: int = int(input("Enter number of answers: ").strip())
        if number_of_questions < 1 or number_of_answers < 1:
            print("Numbers must be greater than 1")
            return False
        test_id = generate_password()
        print(f"Your test id: {test_id}")
        query = '''
        INSERT INTO tests (user_id, name, test_id) VALUES (%s, %s, %s)
        RETURNING ID
        '''
        params = (self.__active_user['id'], test_name, test_id)
        print("Waiting...")
        result = execute_query(query, params, fetch='one')
        self.__test_id = result['id']
        for ques in range(number_of_questions):
            print(f"Question {ques + 1}")
            self.question_func()
            for q_answer in range(number_of_answers):
                print(f'Question: {ques + 1} / Question answer: {q_answer + 1}')
                self.question_answer()
        print(f"Your test id: {self.__test_id}")
        print("Test created successfully")
        return True

    @log_decorator
    def show_all_tests(self):
        pagination = Pagination(table_name='tests', keys=['name', 'test_id', 'status', 'created_at'],
                                user_id=self.__active_user['id'])
        pagination.page_tab()
        return True

    @log_decorator
    def update_test(self):
        test_id: int = int(input("Enter test id: "))
        query = '''
        SELECT * FROM tests WHERE test_id=%s and user_id=%s
        '''
        params = (test_id, self.__active_user['id'])
        get_test = execute_query(query, params, fetch='one')
        if get_test is None:
            print("Test not found")
            return False
        print(f"ID: {get_test['id']}\nName: {get_test['name']}\nCreated at: {get_test['created_at']}")
        name = input("Enter new name: ").strip()
        query = '''
        UPDATE tests SET name=%s WHERE id=%s
        '''
        params = (name, test_id)
        threading.Thread(target=execute_query, args=(query, params)).start()
        return True
