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
        pass
    except Exception as e:
        print(f'Error: {e}')
        auth_menu()
