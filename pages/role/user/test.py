from main_files.decorator.decorator_func import log_decorator


class Test:
    @log_decorator
    def create_table(self):
        pass
