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
    pass


if __name__ == '__main__':
    auth_menu()
