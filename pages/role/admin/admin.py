from components.pagination.pagination import Pagination
from main_files.decorator.decorator_func import log_decorator


class Admin:
    def __init__(self):
        self.__pagination_users = Pagination('users')

    @log_decorator
    def show_all_users(self):
        self.__pagination_users.page_tab()

    @log_decorator
    def update_user(self):
        pass
