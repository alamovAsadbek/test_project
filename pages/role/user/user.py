from main_files.decorator.decorator_func import log_decorator
from pages.role.user.test import Test


class User:
    def __init__(self):
        self.__test = Test()

    @log_decorator
    def create_test(self):
        self.__test.create_test()
        return self.__test

    @log_decorator
    def show_my_tests(self):
        self.__test.show_my_tests()
        return True

    @log_decorator
    def update_test(self):
        self.__test.update_test()
        return True

    @log_decorator
    def delete_test(self):
        self.__test.delete_test()
        return True

    @log_decorator
    def show_all_tests(self):
        self.__test.show_all_tests()
        return True

    @log_decorator
    def join_test(self):
        self.__test.join_test()
        return True

    @log_decorator
    def my_result(self):
        pass
