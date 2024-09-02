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
            check = input("\n1. Yes\t2. No\t\n")
            if check == 1:
                is_true = True
            elif check == 2:
                is_true = False
            else:
                print("Wrong input")
                continue
            break

    @log_decorator
    def question_func(self):
        question_name: str = input("Enter your question: ")
        query = '''
        INSERT INTO questions (name) VALUES (%s)
        RETURNING id
        '''
        params = (question_name,)
        result = execute_query(query, params, fetch='one')
        self.__question_id = result[0]
        return True

    @log_decorator
    def create_test(self):
        test_name: str = input("Enter test name: ").strip()
        number_of_questions: int = int(input("Enter number of questions: ").strip())
        number_of_answers: int = int(input("Enter number of answers: ").strip())
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
        for _ in range(number_of_questions):
            self.question_func()
