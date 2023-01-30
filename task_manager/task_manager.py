"""This module contains a multi user task manager."""
import os
import datetime
import csv

# I've made a few additions to give user the option to list tasks and users
# and also to display the task being edited.

# information on csv module from:
# https://docs.python.org/3/library/csv.html#csv.DictWriter
# https://stackoverflow.com/questions/2363731/how-to-append-a-new-row-to-an-old-csv-file-in-python

# info on datetime module from:
# https://realpython.com/python-datetime/
# https://docs.python.org/3/library/datetime.html

# construct a seperator string we'll use in various places for formatting
seperator = '_' * 80

# construct paths to files
current_dir = os.path.dirname(os.path.abspath(__file__))
user_path = os.path.join(current_dir, "user.txt")
tasks_path = os.path.join(current_dir, "tasks.txt")
task_overview_path = os.path.join(current_dir, "task_overview.txt")
user_overview_path = os.path.join(current_dir, "user_overview.txt")


def main_menu():
    """Display the main menu."""
    while True:
        tasks = read_tasks()
        users = read_users()
        option = get_option(user)

        # ===== Register a user =====
        if option == 'r' and user == 'admin':
            users = reg_user(users)

        # ===== Generate Reports =====
        elif option == 'gr' and user == 'admin':
            generate_reports(tasks)

        # ===== Display statistics for admin =====
        elif option == 'ds' and user == 'admin':
            display_stats(tasks)

        # ===== Add a new task =====
        elif option == 'a':
            tasks = add_task(users, tasks)

        # ===== Display all tasks =====
        elif option == 'va':
            view_all(tasks)

        # ===== Display tasks for logged in user =====
        elif option == 'vm':
            view_mine(user, tasks)

        # ===== Exit Program ====
        elif option == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")


def read_users() -> dict[str, str]:
    """Return a dict of users from users.txt.

    Returns:
        dict containing users
    """
    users = {}
    with open(user_path, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            users[line[0].strip()] = line[1].strip()

    return users


def reg_user(users: dict[str, str]) -> dict[str, str]:
    """Register a user and validate and save their username and password.

    Arguments:
        users -- dict of ersnames and passwords

    Returns:
        dict of users
    """
    # Get username for new user
    username = get_new_username(users)

    # Get password from user
    password = get_new_password()

    # confirm password
    if confirm_password(password):
        # append our new user to file on a new line
        with open(user_path, 'a', newline='') as f:
            csv_line = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            username_pw_pair = [username, password]
            csv_line.writerow(username_pw_pair)
    users[username] = password
    return users


def get_new_username(users: dict[str, str]) -> str:
    """Get a new username from user input.

    Arguments:
        dict of existing usernames and passwords
    Returns:
        new username
    """
    while True:
        name = input(
            "\nPlease enter a username for the new user: ").strip()
        # allow user to exit
        if name == "e":
            print("\nExiting")
            exit()
        # check if username already exists
        elif name in users:
            print(f"""\nError. Username '{name}' already in use.""")
        # check username not blank
        elif len(name) == 0:
            print("\nError. No username entered.")
        else:
            return name


def get_new_password() -> str:
    """Return password from user input.

    Returns:
        user password
    """
    while True:
        password = input(
            "\nPlease enter a password for the new user: ").strip()
        # allow user to exit
        if password == "e":
            print("\nExiting")
            exit()
        # we should at least check that the password meets a minimum length
        elif len(password) < 8:
            print("\nError. Password must be 8 characters or more.")
        else:
            return password


def confirm_password(password: str) -> bool:
    """Ask user to confirm their new password by entering it again.

    Arguments:
        password -- password to confirm

    Returns:
        is password correct
    """
    while True:
        pw_confirmation = input(
            "\nPlease confirm the password: ").strip()
        if pw_confirmation == "e":
            print("\nExiting")
            exit()
        elif pw_confirmation == password:
            return True
        else:
            print(
                "\nError. Passwords do not match.")


def display_stats(tasks: list[dict]):
    """Display stats on number of users and tasks.

    Arguments:
        tasks -- list of tasks
    """
    # regenerate report to ensure it is accurate
    generate_reports(tasks)
    # display reports
    with open(task_overview_path, 'r') as f:
        print(f.read())
    with open(user_overview_path, 'r') as f:
        print(f.read())


def input_task_assignee(users: dict[str, str]) -> str:
    """Return an assignee for a task from user input and check it is valid.

    Arguments:
        users -- dict of users

    Returns:
        assignee
    """
    while True:
        assignee = input("""
Please enter a username to create a new task for them.
l - get a list of existing usernames
b - go back
e - exit
: """).strip().lower()
        if assignee == 'l':
            for user in users.keys():
                print(user)
        elif assignee == 'e':
            print("\nExiting")
            exit()
        elif assignee == 'b':
            main_menu()
        elif assignee not in users.keys():
            print("\nError. User not found.")
        else:
            return assignee


def input_task_title() -> str:
    """Return a task title from user input.

    Returns:
        task title
    """
    while True:
        title = input("""
Please enter a title for the task.
b - go back
e - exit
: """).strip()
        if len(title) < 0:
            print("\nError. Nothing entered.")
        elif title == 'e':
            print("\nExiting")
            exit()
        elif title == 'b':
            main_menu()
        else:
            return title


def input_task_description() -> str:
    """Return a task description from user input.

    Returns:
        task description
    """
    while True:
        description = input("""
Please enter a description for the task
b - go back
e - exit
: """).strip()
        if len(description) < 0:
            print("\nError. Nothing entered.")
        elif description == 'e':
            print("\nExiting")
            exit()
        elif description == 'b':
            main_menu()
        else:
            return description


def add_task(users: dict[str, str], tasks: list[dict]) -> list[dict]:
    """Add a task to tasks.txt based on user input.

    Arguments:
        users -- dict of users
        tasks -- list of tasks
    Returns:
        list of tasks
    """
    assignee = input_task_assignee(users)
    title = input_task_title()
    description = input_task_description()

    # get dates and format
    # https://www.geeksforgeeks.org/how-to-format-date-using-strftime-in-python/
    due_date = get_due_date().strftime("%d %b %Y")
    todays_date = datetime.date.today().strftime("%d %b %Y")

    # construct string to append to file
    line = [assignee, title,
            description, todays_date, due_date, "No"]

    # append task to file on a new line
    # use csv module to escape commas
    with open(tasks_path, mode='a', newline='') as f:
        csv_line = csv.writer(
            f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_line.writerow(line)

    # get num lines in file
    with open(tasks_path, 'r') as f:
        reader = csv.reader(f)
        lines = [x for x in reader]

    # convert task to dict
    task = get_task_dict(lines[-1], len(lines)-1)

    # Print out new task for user
    print_task(task)
    print(f"""
Task Created for {assignee}""")
    tasks.append(task)
    return tasks


def get_due_date() -> datetime.date:
    """Get a due date for a task based on user input.

    Returns:
        due date
    """
    # use datetime module for getting and validating dates
    # https://www.w3schools.com/python/python_datetime.asp
    while True:
        due_date = input("""
Please enter a due date in the following format 'yyyy-mm-dd' e.g. 2022-11-08
b  - go back
e  - exit
: """).strip()
        if due_date == 'e':
            print("\nExiting")
            exit()
        elif due_date == 'b':
            return False
        # we use a try / except block to check that the user has entered
        # a valid date. We could use a stack of if statements here but
        # this is quicker
        try:
            # Convert user string into date object
            # https://docs.python.org/3/library/datetime.html
            due_date = datetime.date.fromisoformat(due_date)
            todays_date = datetime.date.today()
            # make sure our user isn't a time traveller!
            if todays_date > due_date:
                print("\nError. Due date must be in the future.")
            else:
                return due_date
        except ValueError:
            print("\nInvalid date format.")


def print_task(task: dict):
    """Print a task.

    Arguments:
        task -- task to print
    """
    desc_first_line = ''
    desc = task["description"].strip()
    desc_lines = []

    if len(desc) <= 55:
        desc_first_line = desc
        add_lines = False
    else:
        desc_lines = []
        desc_first_line = desc[0:56]
        desc = desc[56:]
        add_lines = True

    while add_lines:
        if len(desc) > 55:
            desc_lines.append(desc[0:55])
            desc = desc[55:]
        else:
            desc_lines.append(desc)
            add_lines = False

    print(f"""{seperator}\n
ID:                     {task['ID']}
Task:                   {task['task'].strip()}
Assigned to:            {task['assigned_user'].strip()}
Date assigned:          {task['date_assigned'].strip()}
Due date:               {task['due_date'].strip()}
Task Complete?          {task['complete'].strip()}
Task Description:       {desc_first_line}""")

    for desc_line in desc_lines:
        print(" " * 24 + desc_line)


def get_task_dict(task: list[str], task_num: int) -> dict[str]:
    """Return a dictionary representation of a task.

    Arguments:
        task -- list representation of task
        task_num -- number of task that corresponds to line number in tasks.txt

    Returns:
        dictionary representation of task
    """
    return {
        "ID": str(task_num),
        "assigned_user": task[0],
        "task": task[1],
        "date_assigned": task[3],
        "due_date": task[4],
        "complete": task[5],
        "description": task[2]}


def get_task_string(task: dict) -> str:
    """Return a string representation of a task for saving to tasks.txt.

    Arguments:
        task -- dict reprresentation of task

    Returns:
        string representation of task
    """
    return f"""{task["assigned_user"]}, {task["task"]}, {task["description"]}\
, {task["date_assigned"]}, {task["due_date"]}, {task["complete"]}"""


def edit_task(task: dict) -> dict:
    """Edit a task.

    Arguments:
        task -- dict representation of task.
    Returns:
        task
    """
    print_task(task)
    if task["complete"].strip() == "No":
        while True:
            option = input(f"""
Please choose from the following options:
ca - change assignee
cd - change due date
b  - go back
e  - exit
: """)
            if option == 'b':
                return task
            elif option == 'e':
                print("\nExiting")
                exit()
            elif option == 'ca':
                return change_assignee(task)
            else:
                return change_due_date(task)
    else:
        print("\nYou cannot edit a task that has already been completed.")
        select_task(read_tasks())


def change_task_element(key: str, value: str, task: dict) -> list:
    """Change element in a dictionary representation of a task.

    Arguments:
        key -- dict key to change
        value -- dict value to change
        task -- dict representation of task
    Returns:
        Task
    """
    # https://www.geeksforgeeks.org/python-program-to-replace-specific-line-in-file/
    # we read in our list of tasks rather than passing it in as a variable as
    # it may have changed
    tasks = read_tasks()
    for t in tasks:
        if t == task:
            t[key] = value
            task = t
            break

    # use csv module to deal with commas etc.
    with open(tasks_path, 'w', newline='') as f:
        fieldnames = ["assigned_user", "task", "description",
                      "date_assigned", "due_date", "complete"]
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=',', quotechar='"',
            quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')

        writer.writerows(tasks)
        # f.writelines(lines)
    return task


def change_assignee(task: dict) -> dict:
    """Change assignee of task.

    Arguments:
        task -- dict representation of task
    Returns:
        task
    """
    users = read_users()
    print_task(task)
    while True:
        new_assignee = input("""
Please enter the name of the new assignee
l  - to get a list of existing users
b  - go back
e  - exit
: """).strip()
        if new_assignee == 'l':
            print("\n")
            for key in users.keys():
                print(key)
        elif new_assignee == 'b':
            return task
        elif new_assignee == 'e':
            print("\nExiting")
            exit()
        elif new_assignee in users.keys():
            task = change_task_element("assigned_user", new_assignee, task)
            print(f"\n{new_assignee} is now assigned to task {task['ID']}")
            print_task(task)
            return task
        else:
            print("\nInvalid input.")


def change_due_date(task: dict) -> dict:
    """Change due date of task.

    Arguments:
        task -- dict representation of task.
    Returns:
        task
    """
    print_task(task)
    due_date = get_due_date().strftime("%d %b %Y")

    task = change_task_element("due_date", due_date, task)
    print(f"\nThe due date for task {task['ID']} is now {due_date}")
    print_task(task)
    return task


def modify_task(task: dict, tasks: list[dict]) -> list[dict]:
    """Present options for modifying task to user.

    Arguments:
        task -- dict representation of task
    Returns:
        list of tasks
    """
    while True:
        edit_option = input("""
Please select one of the following options:
c  - mark task as complete
ed - edit the task
b  - go back
e  - exit
: """).strip().lower()
        if edit_option == 'e':
            print("\nExiting")
            exit()
        elif edit_option == 'b':
            return tasks
        elif edit_option == 'c':
            task = change_task_element("complete", "Yes", task)
            tasks[int(task["ID"])] = task
            print(f"\nTask {task['ID']} complete")
            print_task(task)
            # once we've marked a task as complete back out of edit
            # menu as can no longer edit task
            return tasks
        elif edit_option == 'ed':
            task = edit_task(task)
            tasks[int(task["ID"])] = task
            return tasks
        else:
            print("\nError. Invalid input")


def select_task(tasks: list[dict]):
    """Select task to perform operation on."""
    task_ids = [x["ID"] for x in tasks]
    while True:
        task_id = input(f"""
To select a task please enter the ID number.
-1 - return to main menu
l - list all tasks
e  - exit
: """).strip()
        if task_id == '-1':
            main_menu()
        elif task_id == 'e':
            print("\nExiting")
            exit()
        # give user option to print a list of tasks again so they
        # don't need to scroll up
        elif task_id == 'l':
            for task in tasks:
                print_task(task)
        elif task_id in task_ids:
            # use generator expression to get task
            # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
            task = list(
                (task for task in tasks if task["ID"] == task_id))[0]
            # print task so user can see what they are changing
            print_task(task)
            tasks = modify_task(task, tasks)
        else:
            print("\nInvalid ID.")


def view_all(tasks: list[dict]):
    """View all tasks.

    Arguments:
        tasks -- list of dict representation of tasks
    """
    for task in tasks:
        print_task(task)
    select_task(tasks)


def view_mine(logged_in_user: str, tasks: list[dict]):
    """View all tasks of logged in user.

    Arguments:
        logged_in_user -- username
        tasks -- list of tasks
    """
    user_tasks = [x for x in tasks if x["assigned_user"] == logged_in_user]
    if len(user_tasks) > 0:
        print(f"""\nTasks for {logged_in_user}:""")
        for task in user_tasks:
            print_task(task)

        select_task(user_tasks)
    else:
        print(f"""\n{logged_in_user} has no tasks.""")


def get_option(logged_in_user: str) -> str:
    """Return option from main menu.

    Arguments:
        logged_in_user -- username

    Returns:
        option
    """
    if logged_in_user == "admin":
        option = input('''\nPlease select one of the following options:
r  - register user
a  - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e  - exit
: ''').lower().strip()
        return option
    else:
        option = input('''\nPlease select one of the following options:
a  - add task
va - view all tasks
vm - view my tasks
e  - exit
: ''').lower().strip()
        return option


def task_is_overdue(task: dict) -> bool:
    """Check if task is overdue.

    Arguments:
        task -- dict representation of task

    Returns:
        whether task is overdue
    """
    today = datetime.date.today()
    due_date = datetime.datetime.strptime(task["due_date"], '%d %b %Y').date()
    if today > due_date:
        return True
    return False


def read_tasks() -> list[dict]:
    """Return tasks from file.

    Returns:
        list of dict representation of tasks
    """
    task_list = []
    # Read in tasks from file
    with open(tasks_path, 'r') as f:
        fieldnames = ["assigned_user", "task", "description",
                      "date_assigned", "due_date", "complete"]
        # use .csv reader to handle commas
        tasks = csv.DictReader(f, fieldnames)
        task_list = [x for x in tasks]
        for count, task in enumerate(task_list):
            task["ID"] = str(count)
    return task_list


def generate_reports(tasks: list[dict]):
    """Generate the task_overview.txt and user_overview.txt reports.

    Arguments:
        tasks -- list of tasks
    """
    write_task_overview(tasks)
    write_user_overview(tasks)


def write_task_overview(tasks: list[dict]):
    """Write an overview of tasks to file.

    Arguments:
        tasks -- list of tasks
    """
    num_tasks = len(tasks)
    # count number of completed tasks
    num_completed_tasks = len(
        [x for x in tasks if x["complete"].strip() == "Yes"])
    # get all incomplete tasks
    incomplete_tasks = [x for x in tasks if x["complete"].strip() == "No"]
    num_incomplete = len(incomplete_tasks)

    # count how many incomplete taks are overdue
    overdue_tasks = 0
    for task in incomplete_tasks:
        if task_is_overdue(task):
            overdue_tasks += 1
    # need to check for divide by zero
    perc_overdue = 0
    perc_incomplete = 0
    # calculate percentage of overdue and incomplete tasks
    if num_tasks != 0:
        if overdue_tasks != 0:
            perc_overdue = round((overdue_tasks / num_tasks) * 100)
        if num_incomplete != 0:
            perc_incomplete = round((num_incomplete / num_tasks) * 100)
# construct a string to write to file
    report = f"""
Task Report

{seperator}

Total Tasks:            {num_tasks}
Completed Tasks:        {num_completed_tasks}
Uncompleted Tasks:      {num_incomplete}
Overdue Tasks:          {overdue_tasks}
Percentage Incomplete:  {perc_incomplete} %
Percentage Overdue:     {perc_overdue} %
"""
    # write report to file
    with open(task_overview_path, 'w') as f:
        f.write(report)
    print("\nTask overview report generated")


def write_user_overview(tasks: list[dict]):
    """Write an overview of users to file.

    Arguments:
        tasks -- list of tasks
    """
    users = read_users()
    num_users = len(users)
    num_tasks = len(tasks)
    report = f"""
User Report
{seperator}

Total registered users:             {num_users}
Total tasks:                        {num_tasks}"""
    for user in users:
        user_tasks = [x for x in tasks if x["assigned_user"] == user]
        num_user_tasks = len(user_tasks)
        perc_user_tasks = round((num_user_tasks / num_tasks) * 100)
        user_incomplete = [
            x for x in user_tasks if x["complete"].strip() == "No"]
        num_user_incomplete = len(user_incomplete)

        overdue_tasks = 0
        for task in user_incomplete:
            if task_is_overdue(task):
                overdue_tasks += 1

        # need to check for divide by zero
        perc_user_incomplete = 0
        perc_user_overdue = 0
        perc_user_complete = 0
        if num_user_tasks != 0:
            if num_user_incomplete != 0:
                perc_user_incomplete = round(
                    (num_user_incomplete / num_user_tasks) * 100)
            perc_user_complete = 100 - perc_user_incomplete
            if overdue_tasks != 0:
                perc_user_overdue = round(
                    (overdue_tasks / num_user_tasks) * 100)

        # generate report string
        report = report + f"""
{seperator}

Username:                           {user}
Number of tasks assigned to user:   {num_user_tasks}
% tasks assigned to user:           {perc_user_tasks} %
% user tasks complete               {perc_user_complete} %
% user tasks incomplete             {perc_user_incomplete} %
% user tasks overdue                {perc_user_overdue} %
"""
    with open(user_overview_path, 'w') as f:
        f.write(report)
    print("\nUser overview report generated")


def login_user() -> str:
    """Return username if login is successfull.

    Returns:
        username
    """
    users = read_users()
    # get username
    while True:
        # get username
        username = input("""
Please enter your username: """).strip()
        # give user a way of exiting from loop and exiting program at any time
        if username == "e":
            print("\nExiting")
            exit()
        # check if username exists
        elif username in users:
            check_password(users, username)
            return username.strip().lower()
        else:
            print("\nError. User does not exist.")


def check_password(users: dict, user: str) -> bool:
    """Check if password is valid.

    Arguments:
        users -- dict of users
        user -- username

    Returns:
        true if password is correct
    """
    while True:
        pw_challenge = input("\nPlease enter your password: ")
        if pw_challenge == "e":
            print("\nExiting")
            exit()
        # check user password is correct
        elif users[user] == pw_challenge:
            return True
        else:
            print("\nError. Invalid password.")


print("\nWelcome to the Task Manager. You can enter 'e' at any time to exit.")
user = login_user()
main_menu()
