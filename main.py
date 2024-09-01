from main_files.decorator.decorator_func import log_decorator


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
            pass
        elif user_input == 2:
            pass
        elif user_input == 3:
            pass
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
            pass
        elif user_input == 2:
            pass
        elif user_input == 3:
            pass
        elif user_input == 4:
            pass
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
        pass
    except Exception as e:
        print(f'Error: {e}')
        my_test_menu()


if __name__ == '__main__':
    auth_menu()
