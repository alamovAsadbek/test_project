from components.pagination.pagination import Pagination
from main_files.decorator.decorator_func import log_decorator


class Admin:
    def __init__(self):
        self.__pagination_users = Pagination('users',
                                             ['id', 'first_name', 'last_name', 'username', 'created'])

    @log_decorator
    def show_all_users(self):
        self.__pagination_users.page_tab()
        return True

    @log_decorator
    def get_data(self):
        pass

    @log_decorator
    def update_user(self):
        user_id: int = int(input("Enter user id to update: "))
