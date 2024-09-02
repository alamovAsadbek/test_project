from main_files.decorator.decorator_func import log_decorator


class Pagination:
    def __init__(self, table_name):
        self.table_name = table_name
    @log_decorator
    def read_table(self):
        pass