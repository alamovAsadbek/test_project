from main_files.database.db_setting import get_active_user
from main_files.decorator.decorator_func import log_decorator


class Test:
    def __init__(self):
        self.__active_user = get_active_user()

    @log_decorator
    def create_test(self):
        pass
