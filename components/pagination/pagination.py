import math

from main_files.database.db_setting import execute_query
from main_files.decorator.decorator_func import log_decorator


class Pagination:
    def __init__(self, table_name):
        self.table_name = table_name

    @log_decorator
    def read_table(self):
        query = "SELECT * FROM {}".format(self.table_name)
        return execute_query(query, fetch='all')

    @log_decorator
    def page_tab(self, page_number: int = 1, page_size=2):
        datas = self.read_table()
        while True:
            if datas is None:
                return False
            print(datas[(page_number - 1) * page_size: (page_number - 1) * page_size + page_size])
            print(f"""1 <- {page_number}/{math.ceil(len(datas) / page_size)} -> 2""")
            choice = input("Enter: ")
            if choice == "1":
                if page_number == 1:
                    print("There is no page before that")
                    continue
                page_number -= 1
            elif choice == "2":
                if page_number == math.ceil(len(datas) / page_size):
                    print("There is no page after that")
                    continue
                page_number += 1
            else:
                print("Invalid choice")
