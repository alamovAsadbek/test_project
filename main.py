from main_files.decorator.decorator_func import log_decorator
from pages.auth.auth import Auth


@log_decorator
def auth_menu():
    text = '''
1. Register
2. Login
3. Logout
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            auth.register()
        elif user_input == 2:
            result_login = auth.login()
            if not result_login['is_login']:
                auth_menu()
            elif result_login['role'] == 'user':
                user_menu()
            elif result_login['role'] == 'admin':
                pass
            else:
                print("Something went wrong")
                auth_menu()
        elif user_input == 3:
            auth.logout()
            print("Good bye!")
            return
        else:
            print("Invalid input")
        auth_menu()
    except Exception as e:
        print(f'Error: {e}')
        auth_menu()


@log_decorator
def user_menu():
    text = '''
1. My Tests
2. Tests
3. Statistics
4. Logout
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            print("\n<-\t Home / My Tests\t ->\n")
            my_test_menu()
        elif user_input == 2:
            print("\n<-\t Home / Tests\t ->\n")
            tests_menu()
        elif user_input == 3:
            print("\n<-\t Home / Statistics\t ->\n")
            statistics_menu()
        elif user_input == 4:
            auth_menu()
        else:
            print("Invalid input")
            user_menu()
    except Exception as e:
        print(f'Error: {e}')
        user_menu()


@log_decorator
def my_test_menu():
    text = '''
1. Create new test
2. Update test
3. My tests
4. Delete test
5. Back
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            print("\n<-\t Home / My Tests / Create new test\t ->\n")
            pass
        elif user_input == 2:
            print("\n<-\t Home / My Tests / Update test\t ->\n")
            pass
        elif user_input == 3:
            print("\n<-\t Home / My Tests / My tests\t ->\n")
            pass
        elif user_input == 4:
            print("\n<-\t Home / My Tests / Delete test\t ->\n")
            pass
        elif user_input == 5:
            user_menu()
        else:
            print("Invalid input")
            my_test_menu()
    except Exception as e:
        print(f'Error: {e}')
        my_test_menu()


@log_decorator
def tests_menu():
    text = '''
1. Join test
2. Show all test
3. My results
4. Back
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            print("\n<-\t Home / Tests / Join test\t ->\n")
            pass
        elif user_input == 2:
            print("\n<-\t Home / Tests / Show all test\t ->\n")
            pass
        elif user_input == 3:
            print("\n<-\t Home / Tests / My tests\t ->\n")
            pass
        elif user_input == 4:
            user_menu()
        else:
            print("Invalid input")
            tests_menu()
    except Exception as e:
        print(f'Error: {e}')
        tests_menu()


@log_decorator
def statistics_menu():
    text = '''
1. View statistics on tests
2. Back
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            print("\n<-\t Home / Statistics / View statistics on tests\t ->\n")
            pass
        elif user_input == 2:
            user_menu()
        else:
            print("Invalid input")
            statistics_menu()
    except Exception as e:
        print(f'Error: {e}')
        statistics_menu()


if __name__ == '__main__':
    print("Waiting...")
    auth = Auth()
    auth.logout()
    auth_menu()
