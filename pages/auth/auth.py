from main_files.decorator.decorator_func import log_decorator


class Auth:
    @log_decorator
    def create_user_table(self):
        pass
