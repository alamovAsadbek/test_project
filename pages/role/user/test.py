from components.random_password.generate_password import generate_password
from main_files.database.db_setting import get_active_user
from main_files.decorator.decorator_func import log_decorator


class Test:
    def __init__(self):
        self.__active_user = get_active_user()

    @log_decorator
    def question_func(self):
        pass

    @log_decorator
    def create_test(self):
        test_name: str = input("Enter test name: ").strip()
        number_of_questions: int = int(input("Enter number of questions: ").strip())
        number_of_answers: int = int(input("Enter number of answers: ").strip())
        test_id = generate_password()
        print(f"Your test id: {test_id}")
