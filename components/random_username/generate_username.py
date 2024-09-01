import re
from random import random

from main_files.decorator.decorator_func import log_decorator


@log_decorator
def generate_username(name: str) -> str:
    # Strip and lower case the name
    base_name = name.strip().lower()
    # Replace spaces with underscores
    base_name = base_name.replace(' ', '_')
    # Remove any non-alphanumeric characters except underscores
    base_name = re.sub(r'[^\w]', '', base_name)
    # Generate a random number
    random_number = random.randint(1, 9999)
    return f"{base_name}_{random_number}"
