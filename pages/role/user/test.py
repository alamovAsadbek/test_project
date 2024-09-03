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
        print(f"Your test id: {test_id}")
        print("Test created successfully")
        return True

    @log_decorator
    def show_my_tests(self):
        print("Waiting...")
        pagination = Pagination(table_name='tests', table_keys=['id', 'name', 'test_id', 'status', 'created_at'],
                                display_keys=["ID", "Name", "Test id", "Status", "Created"],
                                user_id=self.__active_user['id'])
        pagination.page_tab()
        return True

    @log_decorator
    def update_test(self):
        test_id: int = int(input("Enter test id and enter 0 to exit: "))
        if test_id == 0:
            return False
        query = '''
        SELECT * FROM tests WHERE id=%s and user_id=%s
        '''
        params = (test_id, self.__active_user['id'])
        get_test = execute_query(query, params, fetch='one')
        if get_test is None:
            print("Test not found")
            return False
        print(f"\nID: {get_test['id']}\nName: {get_test['name']}\nCreated at: {get_test['created_at']}\n")
        name = input("Enter new name: ").strip()
        query = '''
        UPDATE tests SET name=%s WHERE id=%s
        '''
        params = (name, test_id)
        threading.Thread(target=execute_query, args=(query, params)).start()
        print("Updated test successfully")
        return True

    @log_decorator
    def delete_test(self):
        test_id: int = int(input("Enter test id and enter 0 to exit: "))
        if test_id == 0:
            return False
        query = '''
                SELECT * FROM tests WHERE id=%s and user_id=%s
                '''
        params = (test_id, self.__active_user['id'])
        get_test = execute_query(query, params, fetch='one')
        if get_test is None:
            print("Test not found")
            return False
        print(f"\nID: {get_test['id']}\nName: {get_test['name']}\nCreated at: {get_test['created_at']}\n")
        while True:
            print("Do you want to delete this test? (y/n)")
            check = input("Choose (y/n): ")
            if check == 'y':
                query = '''
                DELETE FROM tests WHERE id=%s
                '''
                params = (test_id,)
                threading.Thread(target=execute_query, args=(query, params)).start()
                print("Test deleted successfully")
                return True
            elif check == 'n':
                print("Cancel")
                return True
            else:
                print("Wrong input")
                continue

    @log_decorator
    def show_all_tests(self):
        print("Waiting...")
        query = '''
        SELECT t.test_id, t.name, t.test_id, u.first_name, u.last_name
        FROM tests t
        INNER JOIN users u ON t.user_id = u.id
        WHERE t.user_id != %s;
        '''
        params = (str(self.__active_user['id']),)
        result_get = execute_query(query, params, fetch='all')
        if result_get is None:
            print("Test not found")
            return False
        pagination = Pagination(table_name='tests', table_keys=['name', 'test_id', 'first_name', 'last_name'],
                                display_keys=["Test name", "Test id", "Owner first name", "Owner last name"],
                                data=result_get)
        pagination.page_tab()
        return True

    @log_decorator
    def get_test(self, test_id: int):
        all_tests: dict = dict()
        query = '''
                SELECT * FROM tests WHERE TEST_ID=%s and user_id!=%s
                '''
        params = (test_id, self.__active_user['id'])
        get_test = execute_query(query, params, fetch='one')
        if get_test is None:
            print("Test not found")
            return False
        print(f'\nTEST ID: {get_test["test_id"]}\nTest Name: {get_test["name"]}\n')
        all_tests.update({'test_id': get_test["id"], 'joined_id': get_test["test_id"], 'test_name': get_test["name"],
                          'questions': []})
        print("The test is being prepared...")
        query = '''
                SELECT id, name FROM QUESTIONS WHERE TEST_ID=%s
                '''
        params = (get_test['id'],)
        questions = execute_query(query, params, fetch='all')
        if questions is None:
            print("No test questions found")
            return False
        for index, question in enumerate(questions):
            data = {
                'question_id': question['id'],
                'question_name': question['name'],
            }
            query = '''
            SELECT name, is_true FROM OPTIONS WHERE QUESTION_ID=%s
            '''
            params = (question['id'],)
            options = execute_query(query, params, fetch='all')
            if options is None:
                options = []
            data['options'] = options
            all_tests['questions'].append(data)
        return all_tests

    @log_decorator
    def join_test(self):
        test_id = int(input("Enter test id and enter 0 to exit: ").strip())
        if test_id == 0:
            print("Can't join test")
            return False
        print("Test searching...")
        result_get = self.get_test(test_id=test_id)
        if result_get is False:
            print("Something went wrong")
            return False
        for index, question in enumerate(result_get['questions']):
            print(f"Question {index + 1}")
            print('\n', question['question_name'])
            for index_opt, option in enumerate(question['options']):
                print(f'\t{index_opt + 1}: {option["name"]}')
            while True:
                choose_option: int = int(input("Choose an option: "))
                while choose_option not in range(1, len(question['options']) + 1):
                    print("You have selected the wrong answer. Please select again")
                    choose_option: int = int(input("Choose an option: "))

        print("Test started")
