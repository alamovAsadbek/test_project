import random

from main_files.decorator.decorator_func import log_decorator


@log_decorator
def generate_password() -> int:
    random_num = random.randint(1000, 999999)
    return random_num
