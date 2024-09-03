import math

from main_files.database.db_setting import execute_query
from main_files.decorator.decorator_func import log_decorator


class Pagination:
    def __init__(self, table_name, table_keys, display_keys, user_id=None, data=None):
        self.table_name = table_name
        self.table_keys = table_keys
        self.user_id = user_id
        self.data = data
        self.display_keys = display_keys

    @log_decorator
    def __read_table(self):
        query = "SELECT * FROM {}".format(self.table_name)
        if self.user_id is not None:
            query += " WHERE user_id = '{}'".format(self.user_id)
        return execute_query(query, fetch='all')

    @log_decorator
    def get_page_data(self, page_number=1, page_size=2, table_data=None):
        result_data = table_data[(page_number - 1) * page_size: (page_number - 1) * page_size + page_size]
        return result_data

    @log_decorator
    def page_tab(self, page_number: int = 1, page_size=2):
        datas = self.data
        if datas is None:
            datas = self.__read_table()
        while True:
            if datas is None or len(datas) == 0:
                print("Data not found")
                return False
            result_data = self.get_page_data(page_number, page_size, datas)
            for data in result_data:
                print("\n")
                for display_key, table_key in zip(self.display_keys, self.table_keys):
                    print(f"{display_key}: {data[f'{table_key}']}")
            print(f"""\n1 <- {page_number}/{math.ceil(len(datas) / page_size)} -> 2\n""")
            choice = input("Enter, type exit to exit: ").strip()
            if choice == "exit":
                return True
            elif choice == "1":
                if page_number == 1:
                    print("\nThere is no page before that")
                    continue
                page_number -= 1
            elif choice == "2":
                if page_number == math.ceil(len(datas) / page_size):
                    print("\nThere is no page after that")
                    continue
                page_number += 1
            else:
                print("Invalid choice")
