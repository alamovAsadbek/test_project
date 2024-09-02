import hashlib
import threading

from components.pagination.pagination import Pagination
from main_files.database.db_setting import execute_query
from main_files.decorator.decorator_func import log_decorator


class Admin:
    def __init__(self):
        self.__pagination_users = Pagination('users',
                                             ['id', 'first_name', 'last_name', 'username', 'created'])

    @log_decorator
    def show_all_users(self):
        print("Waiting...")
        self.__pagination_users.page_tab()
        return True

    @log_decorator
    def get_data(self, table_name, data_id):
        query = '''
        SELECT * FROM {} WHERE ID=%s;
        '''.format(
            table_name
        )
        params = (data_id.__str__(),)
        return execute_query(query, params, fetch='one')

    @log_decorator
    def update_user(self):
        user_id: int = int(input("Enter user id to update: "))
        print("Waiting...")
        get_data = self.get_data(table_name='users', data_id=user_id)
        if get_data is None:
            print("User not found")
            return False
        print(f"\nID: {get_data['id']}\nFirst name: {get_data['first_name']}\nLast name: {get_data['last_name']}\n"
              f"Username: {get_data['username']}\n")
        new_password = hashlib.md5(input("Enter new password: ").strip().encode('utf-8')).hexdigest()
        print(new_password)
        query = '''
        UPDATE users SET password=%s WHERE ID=%s;
        '''
        params = (new_password, user_id)
        threading.Thread(target=execute_query, args=(query, params)).start()
        print("Updated successfully")
        return True
