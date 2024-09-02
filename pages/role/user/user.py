from main_files.decorator.decorator_func import log_decorator


class User:
    def __init__(self):
        pass

    @log_decorator
    def create_test(self):
        pass
