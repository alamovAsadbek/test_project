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
    def show_all_tests(self):
        pass
