import threading

from colorama import Fore, init

from components.pagination.pagination import Pagination
from components.random_password.generate_password import generate_password
from main_files.database.db_setting import get_active_user, execute_query
from main_files.decorator.decorator_func import log_decorator


class Test:
    def __init__(self):
        self.__active_user = get_active_user()
        self.__test_id = None
        self.__question_id = None

    @log_decorator
    def question_answer(self):
        """
        Prompts the user to enter an answer for a question and determines if it is the correct answer.
        The answer is then inserted into the database.

        Returns:
        - bool: True if the answer is successfully inserted; False otherwise.
        """

        is_true = False

        # Prompt the user to enter the answer text.
        answer_name: str = input("Enter the answers to the questions: ")

        # Loop to confirm if the entered answer is correct or not.
        while True:
            print("\nIs this the correct answer?")
            print('\n1. Yes\t2. No\t\n')
            check = int(input("Choose: "))

            # Set the flag based on user input.
            if check == 1:
                is_true = True
            elif check == 2:
                is_true = False
            else:
                print("Wrong input")
                continue

            # Confirm the answer and break the loop.
            print("The answer is confirmed")
            break

        # SQL query to insert the answer into the database.
        query = '''
        INSERT INTO options (name, question_id, is_true) VALUES (%s, %s, %s)
        '''

        # Parameters for the query: answer text, question ID, and correctness flag.
        params = (answer_name, self.__question_id, is_true)

        # Execute the query in a separate thread to avoid blocking the main thread.
        threading.Thread(target=execute_query, args=(query, params)).start()

        return True

    @log_decorator
    def question_func(self):
        """
        Prompts the user to enter a question and inserts it into the database.
        The ID of the newly inserted question is stored for further use.

        Returns:
        - bool: True if the question is successfully inserted; False otherwise.
        """

        # Prompt the user to enter the question text.
        question_name: str = input("Enter your question: ")

        # SQL query to insert the question into the database.
        query = '''
        INSERT INTO questions (name, test_id) VALUES (%s, %s)
        RETURNING id
        '''

        # Parameters for the query: question text and test ID.
        params = (question_name, self.__test_id)

        # Execute the query to insert the question and fetch the new ID.
        result = execute_query(query, params, fetch='one')

        # Store the new question ID for further use.
        self.__question_id = result[0]

        return True

    @log_decorator
    def create_test(self):
        """
        Creates a new test with a specified number of questions and answers.
        Prompts the user for test details and iteratively adds questions and answers.

        Returns:
        - bool: True if the test is successfully created; False otherwise.
        """

        # Prompt the user to enter test details.
        test_name: str = input("Enter test name: ").strip()
        number_of_questions: int = int(input("Enter number of questions: ").strip())
        number_of_answers: int = int(input("Enter number of answers: ").strip())

        # Validate the input values.
        if number_of_questions < 1 or number_of_answers < 1:
            print("Numbers must be greater than 1")
            return False

        # Generate a unique test ID.
        test_id = generate_password()
        print(f"Your test id: {test_id}")

        # SQL query to insert the test into the database.
        query = '''
        INSERT INTO tests (user_id, name, test_id) VALUES (%s, %s, %s)
        RETURNING ID
        '''

        # Parameters for the query: user ID, test name, and test ID.
        params = (self.__active_user['id'], test_name, test_id)

        # Execute the query to insert the test and fetch the new ID.
        print("Waiting...")
        result = execute_query(query, params, fetch='one')
        self.__test_id = result['id']

        # Iterate to add questions and answers to the test.
        for ques in range(number_of_questions):
            print(f"Question {ques + 1}")
            self.question_func()
            for q_answer in range(number_of_answers):
                print(f'Question: {ques + 1} / Question answer: {q_answer + 1}')
                self.question_answer()

        # Confirm that the test was created successfully.
        print(f"Your test id: {test_id}")
        print("Test created successfully")

        return True

    @log_decorator
    def show_my_tests(self):
        """
        Displays a paginated list of tests created by the active user.

        Returns:
        - bool: True if the list of tests is successfully displayed; False otherwise.
        """

        print("Waiting...")

        # Initialize pagination for displaying tests.
        pagination = Pagination(table_name='tests', table_keys=['id', 'name', 'test_id', 'status', 'created_at'],
                                display_keys=["ID", "Name", "Test id", "Status", "Created"],
                                user_id=self.__active_user['id'])

        # Display the paginated list of tests.
        pagination.page_tab()

        return True

    @log_decorator
    def update_test(self):
        """
        Updates the name of a test based on the provided test ID.
        The user must provide the test ID and a new name for the test.

        Returns:
        - bool: True if the test is successfully updated; False if the test is not found or the operation is canceled.
        """

        # Prompt the user to enter the test ID they wish to update. Entering 0 will cancel the operation.
        test_id: int = int(input("Enter test id and enter 0 to exit: "))

        # If the user enters 0, cancel the operation and return False.
        if test_id == 0:
            return False

        # SQL query to select the test to be updated, ensuring it belongs to the active user.
        query = '''
        SELECT * FROM tests WHERE id=%s AND user_id=%s
        '''

        # Parameters for the query: test ID and the active user's ID.
        params = (test_id, self.__active_user['id'])

        # Execute the query to fetch the test details.
        get_test = execute_query(query, params, fetch='one')

        # Check if the test was found. If not, notify the user and return False.
        if get_test is None:
            print("Test not found")
            return False

        # Display the details of the test to the user.
        print(f"\nID: {get_test['id']}\nName: {get_test['name']}\nCreated at: {get_test['created_at']}\n")

        # Prompt the user to enter the new name for the test.
        name = input("Enter new name: ").strip()

        # SQL query to update the test name based on its ID.
        query = '''
        UPDATE tests SET name=%s WHERE id=%s
        '''

        # Parameters for the update query: new name and test ID.
        params = (name, test_id)

        # Execute the update query in a separate thread to avoid blocking the main thread.
        threading.Thread(target=execute_query, args=(query, params)).start()

        # Notify the user that the test has been updated successfully.
        print("Updated test successfully")

        # Return True to indicate that the update operation was successful.
        return True

    @log_decorator
    def delete_test(self):
        """
        Allows the active user to delete a test by providing its ID.
        The user is prompted to confirm the deletion before proceeding.

        Returns:
        - bool: True if the test is successfully deleted or the operation is canceled; False otherwise.
        """

        # Prompt the user to enter the test ID they wish to delete. Entering 0 will cancel the operation.
        test_id: int = int(input("Enter test id and enter 0 to exit: "))

        # If the user enters 0, cancel the operation and return False.
        if test_id == 0:
            return False

        # SQL query to select the test to be deleted, ensuring it belongs to the active user.
        query = '''
        SELECT * FROM tests WHERE id=%s AND user_id=%s
        '''

        # Parameters for the query: test ID and the active user's ID.
        params = (test_id, self.__active_user['id'])

        # Execute the query to fetch the test details.
        get_test = execute_query(query, params, fetch='one')

        # Check if the test was found. If not, notify the user and return False.
        if get_test is None:
            print("Test not found")
            return False

        # Display the details of the test to the user for confirmation.
        print(f"\nID: {get_test['id']}\nName: {get_test['name']}\nCreated at: {get_test['created_at']}\n")

        # Prompt the user to confirm if they really want to delete the test.
        while True:
            print("Do you want to delete this test? (y/n)")
            check = input("Choose (y/n): ")

            # If the user confirms (enters 'y'), proceed with deletion.
            if check == 'y':
                # SQL query to delete the test based on its ID.
                query = '''
                DELETE FROM tests WHERE id=%s
                '''
                # Parameters for the deletion query: test ID.
                params = (test_id,)

                # Execute the deletion query in a separate thread to avoid blocking the main thread.
                threading.Thread(target=execute_query, args=(query, params)).start()

                # Notify the user that the test was deleted successfully and return True.
                print("Test deleted successfully")
                return True

            # If the user cancels (enters 'n'), print a cancel message and return True.
            elif check == 'n':
                print("Cancel")
                return True

            # If the input is invalid, prompt the user to enter 'y' or 'n' again.
            else:
                print("Wrong input")
                continue

    @log_decorator
    def show_all_tests(self):
        """
        Retrieves and displays all tests that are not created by the active user,
        along with the names of their creators. Uses pagination to display the results.

        Returns:
        - bool: True if tests are found and displayed successfully; False otherwise.
        """

        # Notify the user that the operation is in progress.
        print("Waiting...")

        # SQL query to select tests created by users other than the active user.
        query = '''
        SELECT t.test_id, t.name, t.test_id, u.first_name, u.last_name
        FROM tests t
        INNER JOIN users u ON t.user_id = u.id
        WHERE t.user_id != %s;
        '''

        # Parameters for the SQL query to exclude tests created by the active user.
        params = (str(self.__active_user['id']),)

        # Execute the query to fetch all relevant tests.
        result_get = execute_query(query, params, fetch='all')

        # Check if the query returned any results.
        if result_get is None:
            print("Test not found")
            return False

        # Initialize pagination for displaying the results.
        pagination = Pagination(
            table_name='tests',
            table_keys=['name', 'test_id', 'first_name', 'last_name'],
            display_keys=["Test name", "Test id", "Owner first name", "Owner last name"],
            data=result_get
        )

        # Display the paginated results.
        pagination.page_tab()

        # Indicate that the operation was successful.
        return True

    @log_decorator
    def get_test(self, test_id: int):
        """
        Retrieves details of a specific test, including its questions and options,
        from the database. Returns a dictionary with test details and questions.

        Parameters:
        - test_id (int): The ID of the test to retrieve.

        Returns:
        - dict: A dictionary containing test details, including questions and options.
        """

        # Initialize an empty dictionary to hold the test details and questions.
        all_tests: dict = dict()

        # SQL query to select test details where TEST_ID matches and the test is not created by the active user.
        query = '''
        SELECT * FROM tests WHERE TEST_ID=%s and user_id!=%s
        '''

        # Parameters for the SQL query.
        params = (test_id, self.__active_user['id'])

        # Execute the query to retrieve the test details.
        get_test = execute_query(query, params, fetch='one')

        # If no test is found, print a message and return False.
        if get_test is None:
            print("Test not found")
            return False

        # Print the retrieved test details.
        print(f'\nTEST ID: {get_test["test_id"]}\nTest Name: {get_test["name"]}\n')

        # Update the all_tests dictionary with test details and an empty list for questions.
        all_tests.update({
            'test_id': get_test["id"],
            'joined_id': get_test["test_id"],
            'test_name': get_test["name"],
            'questions': []
        })

        # Notify that the test is being prepared.
        print("The test is being prepared...")

        # SQL query to retrieve all questions for the given test ID.
        query = '''
        SELECT id, name FROM QUESTIONS WHERE TEST_ID=%s
        '''

        # Parameters for the SQL query to fetch questions.
        params = (get_test['id'],)

        # Execute the query to retrieve the questions.
        questions = execute_query(query, params, fetch='all')

        # If no questions are found, print a message and return False.
        if questions is None:
            print("No test questions found")
            return False

        # Iterate over each question and retrieve its options.
        for index, question in enumerate(questions):
            # Prepare a dictionary for each question.
            data = {
                'question_id': question['id'],
                'question_name': question['name'],
            }

            # SQL query to retrieve options for a specific question ID.
            query = '''
            SELECT id, name, is_true FROM OPTIONS WHERE QUESTION_ID=%s
            '''

            # Parameters for the SQL query to fetch options.
            params = (question['id'],)

            # Execute the query to retrieve the options.
            options = execute_query(query, params, fetch='all')

            # If no options are found, set options to an empty list.
            if options is None:
                options = []

            # Add options to the question data.
            data['options'] = options

            # Append the question data to the all_tests dictionary.
            all_tests['questions'].append(data)

        # Return the dictionary containing test details and questions.
        return all_tests

    @log_decorator
    def insert_answer_table(self, test_id):
        """
        Inserts a new record into the 'answers' table with initial values for
        CORRECT_ANSWERS and WRONG_ANSWERS set to 0, and returns the ID of the new record.

        Parameters:
        - test_id (int): The ID of the test for which the answer record is being created.

        Returns:
        - int: The ID of the newly created answer record.
        """

        # SQL query to insert a new record into the 'answers' table and return the new record's ID.
        query = '''
        INSERT INTO answers (user_id, test_id, CORRECT_ANSWERS, WRONG_ANSWERS) 
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        '''

        # Parameters to be used in the SQL query.
        # Converts user ID to string, sets initial counts for correct and wrong answers to 0.
        params = (str(self.__active_user['id']), test_id, 0, 0)

        # Execute the query with the specified parameters.
        # Fetches the ID of the newly inserted record.
        result = execute_query(query, params, fetch='one')

        # Return the ID of the newly inserted record.
        return result['id']

    @log_decorator
    def join_test(self):
        # Initialize counters for the number of correct and wrong answers
        current_answer = 0
        wrong_answer = 0

        # Initialize Colorama to automatically reset text color after each print statement
        init(autoreset=True)

        # Get the test ID from user input
        test_id = int(input("Enter test id and enter 0 to exit: ").strip())

        # If user enters 0, exit the method
        if test_id == 0:
            print("Can't join test")
            return False

        # Indicate that the test is being searched for
        print("Test searching...")

        # Fetch test details using the provided test ID
        result_get = self.get_test(test_id=test_id)

        # Insert a new record into the answers table for the user and get the answer ID
        get_answer_id = self.insert_answer_table(test_id=result_get["test_id"])

        # If fetching the test details failed, inform the user and exit the method
        if result_get is False:
            print("Something went wrong")
            return False

        # Loop through each question in the fetched test
        for index, question in enumerate(result_get['questions']):
            # Display the question
            print(f"Question {index + 1}")
            print('\n', question['question_name'])

            # Display the options for the current question
            for index_opt, option in enumerate(question['options']):
                print(f'\t{index_opt + 1}: {option["name"]}')

            # Get the user's choice of option
            choose_option: int = int(input("Choose an option: "))

            # Validate the user's choice; it must be within the valid range of options
            while choose_option not in range(1, len(question['options']) + 1):
                print(Fore.RED + "You have selected the wrong answer. Please select again")
                choose_option: int = int(input(Fore.BLUE + "\tChoose an option: "))

            # Get the selected option based on the user's choice
            select_option = result_get['questions'][index]['options'][choose_option - 1]

            # Check if the selected option is correct or not
            if select_option['is_true']:
                print(Fore.GREEN + "Your answer is correct")
                current_answer += 1
            else:
                print(Fore.RED + "Your answer is incorrect")
                wrong_answer += 1

            # Insert the answer record into the answer_items table
            query = '''
            INSERT INTO answer_items (user_id, question_id, is_true, answer_id) VALUES (%s, %s, %s, %s)
            '''
            params = (
                str(self.__active_user['id']), question['question_id'].__str__(), True, get_answer_id)
            threading.Thread(target=execute_query, args=(query, params)).start()

        # Print summary of the test results
        print(f"\nNumber of questions: {len(result_get['questions'])}\n"
              f"Current answer: {current_answer}\n"
              f"Wrong answer: {wrong_answer}")

        # Update the answers table with the final count of correct and wrong answers
        query = '''
        UPDATE ANSWERS SET CORRECT_ANSWERS=%s, WRONG_ANSWERS=%s WHERE id=%s
        '''
        params = (current_answer, wrong_answer, get_answer_id)
        threading.Thread(target=execute_query, args=(query, params)).start()

        # Inform the user that the test is over
        print("\nThe test is over\n")
        return True

    @log_decorator
    def my_results(self):
        query = '''
        SELECT a.correct_answers, a.wrong_answers, t.name, t.test_id
        FROM tests t
        INNER JOIN answers a ON t.id = a.test_id
        WHERE a.user_id = %s
        '''
        params = (str(self.__active_user['id']),)
        results = execute_query(query, params, fetch='all')
        if results is None:
            print("Test not found")
            return False
        for index, test in enumerate(results):
            print(f"\n№ {index + 1}\nTest name: {test['name']}\nTest ID: {test['test_id']}\n"
                  f"Correct answers: {test['correct_answers']}\nWrong answers: {test['wrong_answers']}\n")
        return True

    @log_decorator
    def view_statistics_on_tests(self):
        query = '''
        SELECT usr.first_name, usr.last_name, usr.username, t.name, t.test_id, a.correct_answers, a.wrong_answers, 
        FROM USERS u
        INNER JOIN TESTS t ON u.id = t.user_id
        INNER JOIN ANSWERS a ON t.id = a.test_id
        INNER JOIN users usr ON a.user_id = usr.id
        where u.id = 4;
        '''
        params = (str(self.__active_user['id']),)
        result_get = execute_query(query, params, fetch='all')
        print(result_get)
