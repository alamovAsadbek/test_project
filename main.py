from main_files.decorator.decorator_func import log_decorator
from pages.auth.auth import Auth
from pages.role.admin.admin import Admin
from pages.role.user.user import User


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
                admin_menu()
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
def admin_menu():
    text = '''
1. Show all users
2. Update user
3. Logout
    '''
    print(text)
    try:
        admin = Admin()
        admin_input: int = int(input("Choose menu: "))
        if admin_input == 1:
            admin.show_all_users()
        elif admin_input == 2:
            admin.update_user()
        elif admin_input == 3:
            return auth_menu()
        else:
            print("Invalid input")
        admin_menu()
    except Exception as e:
        print(f'Error: {e}')
        admin_menu()


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
            print("Waiting...")
            auth.logout()
            auth_menu()
        else:
            print("Invalid input")
            user_menu()
    except Exception as e:
        print(f'Error: {e}')
        user_menu()


@log_decorator
def my_test_menu():
    print("Waiting...")
    user = User()
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
            user.create_test()
        elif user_input == 2:
            print("\n<-\t Home / My Tests / Update test\t ->\n")
            user.update_test()
        elif user_input == 3:
            print("\n<-\t Home / My Tests / My tests\t ->\n")
            user.show_my_tests()
        elif user_input == 4:
            print("\n<-\t Home / My Tests / Delete test\t ->\n")
            user.delete_test()
        elif user_input == 5:
            return user_menu()
        else:
            print("Invalid input")
        my_test_menu()
    except Exception as e:
        print(f'Error: {e}')
        my_test_menu()


@log_decorator
def tests_menu():
    print("Waiting...")
    user = User()
    text = '''
1. Join test
2. Show all tests
3. My results
4. Back
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            print("\n<-\t Home / Tests / Join test\t ->\n")
            user.join_test()
        elif user_input == 2:
            print("\n<-\t Home / Tests / Show all tests\t ->\n")
            user.show_all_tests()
        elif user_input == 3:
            print("\n<-\t Home / Tests / My tests\t ->\n")
            user.my_result()
        elif user_input == 4:
            return user_menu()
        else:
            print("Invalid input")
        tests_menu()
    except Exception as e:
        print(f'Error: {e}')
        tests_menu()


@log_decorator
def statistics_menu():
    print("Waiting...")
    user = User()
    text = '''
1. View statistics on tests
2. View statistics on test questions
3. Back
    '''
    print(text)
    try:

        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            print("\n<-\t Home / Statistics / View statistics on tests\t ->\n")
            print("Waiting...")
            user.statistics_test()
        elif user_input == 2:
            print("\n<-\t Home / Statistics / View statistics on test questions\t ->\n")
            print('Waiting....')
            user.statistics_test_questions()
        elif user_input == 3:
            return user_menu()
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
