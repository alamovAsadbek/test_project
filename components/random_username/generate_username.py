import random
import re

from main_files.database.db_setting import execute_query
from main_files.decorator.decorator_func import log_decorator


@log_decorator
def __generate_username(name: str) -> str:
    # Strip and lower case the name
    base_name = name.strip().lower()
    # Replace spaces with underscores
    base_name = base_name.replace(' ', '_')
    # Remove any non-alphanumeric characters except underscores
    base_name = re.sub(r'\W', '', base_name)
    # Generate a random number
    random_number = random.randint(1, 9999)
    return f"{base_name}_{random_number}"


@log_decorator
def get_username(name: str) -> str:
    while True:
        username = __generate_username(name)
        query = '''
         SELECT * FROM users WHERE USERNAME=%s;
         '''
        params = (username,)
        result = execute_query(query, params, fetch='one')
        if result is not None:
            continue
        return username
