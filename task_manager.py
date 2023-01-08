# =====importing libraries===========
import datetime as dt
from collections import defaultdict
import os

# =====terminal colour customization===========
WARNING = "\033[93m"
RESET = "\033[0m"

# ====Function Section====


# display menu function
def display_menu(user: str):
    # check if user is admin, display different menu to admin
    # making sure that the user input is converted to lower case. for error handling
    if user != 'admin':
        choice = input('''\nSelect one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()
    else:
        choice = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - Generate report
ds - Display statistics
e - Exit
: ''').lower()

    return choice


# register user function
def reg_user(user: str, data: dict):
    # check if the user is the admin, display message if not
    if user == "admin":
        # loop while user exists in database
        while True:
            # ask user for new username, password, and password confirmation
            new_username = input("Please input the new username: ")
            # check if user exists
            if new_username not in data:
                new_password = input("Please input the new password: ")
                pass_confirmation = input("Please confirm the password: ")

                # check passwords match
                if new_password == pass_confirmation:
                    # if passwords match, open users.txt in append mode and write data, break from loop
                    with open(file="./user.txt", mode="a") as users_file:
                        users_file.write(f"\n{new_username}, {new_password}")
                        # print new line for clarity
                        print("\n")
                    break
                else:
                    print("The passwords do not match!\n")
                    continue
            else:
                print(f"user '{new_username}' already exists, please try again.")
                continue
    else:
        print("\nOnly the administrator can register a new user!\n")


# add task function
def add_task(data: dict):
    # ask for username
    task_username = input("Enter the user name of task assignee: ")

    # check if username is valid, display message if not
    if task_username in data:
        # ask for task data: title, desc, due-date
        task_title = input("Enter the task title: ")
        task_desc = input("Enter the task description: ")
        task_due_date = input("Enter the task due date\n(in the format dd mmm yyyy e.g. 12 Jan 2025): ")

        # get today's date with date time module and strftime method
        today_date = dt.datetime.today().strftime("%d %b %Y")

        # set task complete to No
        task_complete = "No"

        # open tasks.txt in append mode
        with open(file="./tasks.txt", mode="a") as tasks_file:
            # write data to tasks file
            tasks_file.write(f"{task_username}, {task_title}, {task_desc}, {today_date}, {task_due_date}, "
                             f"{task_complete}\n")
    else:
        print("Cannot assign a task to a non-existent user!\n")


# get task data function
def get_tasks(user: str = "All users", data_only: bool = False) -> dict:
    # get task data in read mode
    with open(file="./tasks.txt", mode="r") as task_file:
        # read data to list
        task_data = task_file.readlines()
        task_data = [data.strip("\n").split(", ") for data in task_data]

        # use default dict to generate dictionary with key as user
        # and value as list of lists with task information
        # ref. https://docs.python.org/3/library/collections.html#collections.defaultdict
        task_dict = defaultdict(list)

        # loop through original list, append data to corresponding users in dictionary
        for element in task_data:
            task_dict[element[0]].append(element[1:])

        # check if only dictionary data required from function (without display), return if true (false by default)
        if data_only:
            return task_dict

        # display results if user has tasks, else display all tasks
        if user in task_dict:
            # enumerate for task numbers, start at 1 for user-friendliness.
            # will need to compensate when indexing tasks by subtracting 1 (i - 1)
            for i, item in enumerate(task_dict[user], start=1):
                # display tasks
                print(
                    f"""
                ----------------------------------------------
                No. {i}
                Task:               {task_dict[user][i - 1][0]}
                Date Assigned:      {task_dict[user][i - 1][2]}
                Due date:           {task_dict[user][i - 1][3]}
                Task Complete?      {task_dict[user][i - 1][4]}
                Task Description:
                    {task_dict[user][i - 1][1]}
                ----------------------------------------------
                """
                )

        else:
            for user in task_dict:
                for item in task_dict[user]:
                    print(
                        f"""
                ----------------------------------------------
                Task:               {item[0]}
                Assigned To:        {user}
                Date Assigned:      {item[2]}
                Due date:           {item[3]}
                Task Complete?      {item[4]}
                Task Description:
                    {item[1]}
                ----------------------------------------------
                """
                    )
        return task_dict


# view all tasks function
def view_all():
    # get task data from get tasks function (all user tasks as default)
    get_tasks()


# view user tasks function
def view_mine(user: str, user_credentials: dict):

    # set variable data_modified to false
    data_modified = False

    # run function to print task data for user, get dictionary for data processing from function
    task_dict = get_tasks(user)

    # if user in task dictionary, proceed, otherwise display message
    if user in task_dict:
        # loop until correct number or -1 selected, data will only be updated when -1 selected (if flag set to true)
        while True:
            # give user choice, cast to integer for indexing (subtract 1 because of enumerate function)
            choice = int(input("Which task would you like to update "
                               "(enter a number,\n -1 to return to main menu)? "))

            # create list of task numbers
            task_numbers = list(range(len(task_dict[user])))

            # # including -1 for exit option
            # task_numbers.append(-1)

            if choice == -1:
                break
            elif choice-1 in task_numbers:
                # ask action, lower for error handling
                action = input("\nWould you like to mark this task as complete"
                               "\nor edit the due date or reassign? (enter c, d, or ta) ").lower()

                # check task isn't complete, display message otherwise
                if task_dict[user][choice - 1][-1] != "Yes":
                    # pattern match on action
                    match action:
                        case "c":
                            # change last element of list to Yes
                            task_dict[user][choice - 1][-1] = "Yes"

                            # set data_modified flag to true, break from loop
                            data_modified = True

                        case "d":
                            new_date = input("\nEnter the new due date (DD MMM YYYY): ")

                            # update the date
                            task_dict[user][choice - 1][3] = new_date

                            # set data_modified flag to true
                            data_modified = True

                        case "ta":
                            # loop until existing user entered
                            while True:
                                # ask for new assignee
                                new_task_assignee = input("\nEnter the new task assignee: ")
                                if new_task_assignee in user_credentials:
                                    # remove task from logged-in user
                                    task_to_move = task_dict[user].pop(choice - 1)

                                    # move task to specified user
                                    task_dict[new_task_assignee].append(task_to_move)

                                    # set data_modified flag to true, break from loop
                                    data_modified = True
                                    break
                                else:
                                    print(f"\n'{new_task_assignee}' is not a registered user")

                        case _:
                            print(f"\n{action} is not a valid option, try again.")
                else:
                    print(f"\nTask {choice} is already complete!")

            else:
                print(f"\n{choice} is not a valid task number, try again.")
                break

    else:
        print(f"\n there are no tasks for {user}\n")

    # update task file only if data_modified flag is true
    if data_modified:
        with open("./tasks.txt", "w") as updated_tasks:
            # declare empty string variable for concatenation
            all_data = ""

            # loop through users in task_dict
            for user in task_dict:
                # loop through users tasks
                for item in task_dict[user]:
                    # formate data for output (same order as other function (-1 on index
                    # numbers because of new data structure)
                    all_data += f"{user}, {item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]}\n"

            # write data to tasks file
            updated_tasks.write(all_data)


# generate report function
def generate_report():
    # get today's date with date time module
    today_date = dt.datetime.today()

    # get data from task files, with data only as true (to stop data printing)
    task_dict = get_tasks(data_only=True)

    # create variable for total number of tasks, initialize to 0
    total_tasks: int = 0

    # create variable for completed tasks, initialize to 0
    completed_tasks: int = 0

    # create variable for incomplete tasks, initialize to 0
    incomplete_tasks: int = 0

    # create variable for overdue tasks, initialize to 0
    overdue_tasks: int = 0

    # get total number of users from users file in read mode
    with open(file="./user.txt", mode="r") as users_file:
        # read file to list and calculate length to get number of users
        total_users = len(users_file.readlines())

    """
    The following lines of code create 3 dictionaries, one with users and completed tasks, the other with users
    and incomplete tasks, finally one with users and overdue tasks.
    This works with a dictionary comprehension and a nested list comprehension.
    The dictionary comprehension loops through the keys (users) in the task_dict, 
    the list comprehension checks the tasks associated with the user and only adds it to the list if contains 
    the complete flag ("Yes") or the incomplete flag ("No") in the case of the incomplete tasks 
    (with a date comparison on the overdue tasks)
    """
    complete_user_tasks = {
        user: [task for task in task_dict[user] if "Yes" in task] for user in task_dict
    }

    incomplete_user_tasks = {
        user: [task for task in task_dict[user] if "No" in task] for user in task_dict
    }

    overdue_user_tasks = {
        user: [
            task for task in task_dict[user] if "No" in task and dt.datetime.strptime(task[3], "%d %b %Y") < today_date
        ] for user in task_dict
    }

    # loop through task_dict and populate data
    for user in task_dict:
        total_tasks += len(task_dict[user])
        for task in task_dict[user]:
            # convert task due date to datetime object (for comparison)
            task_due_date = dt.datetime.strptime(task[3], "%d %b %Y")

            # check task is complete, increment completed_tasks if true
            if "Yes" in task:
                completed_tasks += 1

            # check task is incomplete, increment incomplete_tasks if true
            if "No" in task:
                incomplete_tasks += 1

            # check task is incomplete and overdue, increment overdue_tasks if true
            if "No" in task and task_due_date < today_date:
                overdue_tasks += 1

    # check if total tasks not equal 0 to avoid ZeroDivision Error
    if total_tasks != 0:
        # define incomplete percentage variable  and calculate (round to 2 dp)
        incomplete_tasks_percentage = round((incomplete_tasks / total_tasks) * 100, 2)

        # define overdue percentage variable  and calculate (round to 2 dp)
        overdue_tasks_percentage = round((overdue_tasks / total_tasks) * 100, 2)
    else:
        # set both percentage variables to 0
        incomplete_tasks_percentage = 0
        overdue_tasks_percentage = 0

    # open task_overview file in write mode
    with open(file="./task_overview.txt", mode="w") as task_overview:
        # declare string and assign formatted data
        task_overview_string = f"""Task Overview
-------------
Total number of tasks:      {total_tasks}
Number completed:           {completed_tasks}
Number incomplete:          {incomplete_tasks}
Percent incomplete:         {incomplete_tasks_percentage}%
Percent overdue:            {overdue_tasks_percentage}%
-------------
"""
        # write formatted data to task overview file
        task_overview.write(task_overview_string)

    # open user_overview file in write mode
    with open(file="./user_overview.txt", mode="w") as user_overview:
        user_overview_string = f"""User Overview
-------------
Total number of users:      {total_users}
Total number of tasks:      {total_tasks}
-------------

"""
        # loop through task dict and use previously generated dictionaries (lines 290-302) to calculate/get data
        for user in task_dict:
            # declare variables, calculate statistics and round to 2 decimal places
            total_tasks_user = len(task_dict[user])
            total_tasks_user_percent = round((len(task_dict[user]) / total_tasks) * 100, 2)
            tasks_user_complete_percent = round((len(complete_user_tasks[user]) / total_tasks_user) * 100, 2)
            tasks_left_percent = round((len(incomplete_user_tasks[user]) / total_tasks_user) * 100, 2)
            overdue_user_tasks_percentage = round((len(overdue_user_tasks[user]) / total_tasks_user) * 100, 2)

            # concatenate variables to string per user
            user_overview_string += f"""User: {user}
-------------
Total tasks assigned:       {total_tasks_user}
Total tasks percentage:     {total_tasks_user_percent}%
Tasks complete percentage:  {tasks_user_complete_percent}%
Tasks left percentage:      {tasks_left_percent}%
Overdue tasks percentage:   {overdue_user_tasks_percentage}%
-------------

"""

        # write formatted data to user overview file
        user_overview.write(user_overview_string)


# statistics function, returns tuple of data
def get_stats() -> tuple:
    # open task overview file and get data
    with open(file="./task_overview.txt", mode="r") as task_overview_file:
        task_overview_data = task_overview_file.read()
    # open user over file and get data
    with open(file="./user_overview.txt", mode="r") as user_overview_file:
        user_overview_data = user_overview_file.read()

    # return data as tuple for unpacking
    return task_overview_data, user_overview_data

# ====Login Section====


# open user.txt in read only with alias 'users'
with open(file="./user.txt", mode="r") as users:
    # read data to list
    user_data = users.readlines()

    # use dictionary comprehension to populate dictionary with usernames and passwords
    user_info = {
        # split the data into a list on whitespace, strip the comma from the first element, assign as key
        # split the data into a list on whitespace, get second item, assign as value of key
        data.split()[0].strip(","): data.split()[1] for data in user_data
    }

# declare boolean to break out of while loop when logged in
logged_in = False

# ask for username and password until correct details entered
while True:
    # only ask for user and pass if not logged in
    if logged_in is False:
        username = input("Enter your user name: ")
        password = input("Enter your user password: ")

    # check if logged in
    if logged_in is True:
        # print new line for clarity, and break out of loop
        print("\n")
        break
    
    # check username exists, check password is correct
    if username not in user_info:
        print("This user does not exit, please try again\n")
    elif user_info[username] != password:
        print("You entered an incorrect password, please try again\n")
    else:
        # user and pass match, set logged in to true and break out of loop
        logged_in = True
        break

while True:
    # pass username into display function and present appropriate menu
    menu = display_menu(username)

    if menu == 'r':
        # pass username and user data into function (will only function if username is admin)
        reg_user(username, user_info)

    elif menu == 'a':
        # run add task function with user data as argument
        add_task(user_info)

    elif menu == 'va':
        # run view all tasks function
        view_all()

    elif menu == 'vm':
        # run view mine function with username and user info as arguments
        view_mine(username, user_info)
    # only run the reports if the user is the admin (incase other user presses ds by accident)
    elif menu == "gr" and username == "admin":
        generate_report()

    # only run the stats if the user is the admin (incase other user presses ds by accident)
    elif menu == "ds" and username == "admin":
        # check data files for stats exist using os module and exists function
        # run generate reports if files don't exist
        task_overview = "./task_overview.txt"
        user_overview = "./user_overview.txt"
        if os.path.exists(task_overview) and os.path.exists(user_overview):
            # in case of existing data files, tell admin to update report for most recent stats
            print(f"{WARNING}Note: Update the report with 'gr' for most recent stats{RESET}\n")

            # use deconstruction to assign data from show_stats to variables
            task_overview_stats, user_overview_stats = get_stats()

            # print stats to console
            print(task_overview_stats)
            print(user_overview_stats)
        else:
            # run generate reports if data files don't exist
            generate_report()
            # use deconstruction to assign data from show_stats to variables
            task_overview_stats, user_overview_stats = get_stats()

            # print stats to console
            print(task_overview_stats)
            print(user_overview_stats)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again\n")
