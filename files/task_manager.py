# =====importing libraries===========
import os
import datetime

# construct a seperator string we'll use in various places for formatting
seperator = '_' * 80

# ====Login Section====
# get current directory so we can find tasks files
current_dir = os.path.dirname(os.path.abspath(__file__))

# construct paths to files
user_path = os.path.join(current_dir, "user.txt")
tasks_path = os.path.join(current_dir, "tasks.txt")


# store usernames and passwords in dict
# https://www.w3schools.com/python/python_dictionaries.asp
# we're going to do this several times to avoid having to keep the dict and
# the password file in sync so wrapping this in a function
def get_passwords() -> dict:
    passwords = {}
    with open(user_path, 'r') as f:
        for line in f:
            user = line.split(', ')
            # strip whitespace including the \n character which will
            # otherwise cause problems when checking passwords.
            passwords[user[0].strip()] = user[1].strip()
    return passwords


logged_in_user = ''
valid_username = False
passwords = get_passwords()

print("\nWelcome to the Task Manager. You can enter 'e' at any time to exit.")

# get username
while not valid_username:
    # get username
    name = input("\nPlease enter your username: ").strip()

    # give user a way of exiting from loop and exiting program at any time
    if name == "e":
        print("\nExiting")
        exit()
    # check if username exists
    elif name in passwords:
        logged_in_user = name
        valid_username = True
    else:
        print("\nError. User does not exist.")

# We could embed this in the check username while loop, however keeping it
# seperate is better for readability
password = ''
valid_password = False
while not valid_password:
    pw_challenge = input("\nPlease enter your password: ")
    if pw_challenge == "e":
        print("\nExiting")
        exit()
    # check user password is correct
    elif passwords[logged_in_user] == pw_challenge:
        valid_password = True
    else:
        print("\nError. Invalid password.")

# =====Options Section=====

while True:
    # present the menu to the user and make sure that the user input is
    # converted to lower case. Also strip whitespace
    # admins and non admins get different options
    if logged_in_user == "admin":
        menu = input('''\nPlease select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
s - display statistics
e - exit
: ''').lower().strip()

    else:
        menu = input('''\nPlease select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').lower().strip()

# ===== Register a user =====
    if menu == 'r' and logged_in_user == 'admin':
        # we need to read in from our passwords file again here. This is a
        # design decision as otherwise we have to keep our dict synced with our
        # file as we add users in.
        passwords = get_passwords()
        username = ''
        valid_username = False
        while not valid_username:
            name = input(
                "\nPlease enter a username for the new user: ").strip()
            # allow user to exit
            if name == "e":
                print("\nExiting")
                exit()
            # check if username already exists
            elif name in passwords:
                print(f"""\nError. Username '{name}' already in use.""")
            # check username not blank
            elif len(name) == 0:
                print("\nError. No username entered.")
            else:
                username = name
                valid_username = True

        # Get password from user
        password = ''
        valid_password = False
        while not valid_password:
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
                valid_password = True

                # ask user to re-enter password and check they match
                pw_confirmation = ''
                matched_passwords = False

                while not matched_passwords:
                    pw_confirmation = input(
                        "\nPlease confirm the password: ").strip()
                    if pw_confirmation == "e":
                        print("\nExiting")
                        exit()
                    elif pw_confirmation == password:
                        print(f"""New user {username} added""")
                        matched_passwords = True
                    else:
                        print(
                            "\nError. Passwords do not match.")

        # append our new user to file on a new line
        with open(user_path, 'a') as f:
            f.write(f"""\n{username}, {password}""")

        # we could add new user to password keys here but it is probably
        # better in practice to always get usernames and pws from the file
        # instead of trying to keep them synced

    # ===== Display statistics for admin =====
    elif menu == 's' and logged_in_user == 'admin':
        with open(user_path, 'r') as f:
            num_users = len(f.readlines())
        with open(tasks_path, 'r') as f:
            num_tasks = len(f.readlines())

        print(f"""\nTask Manager Statistics:
{seperator}

Total number of tasks:      {num_tasks}
Total number of users:      {num_users}
{seperator}""")

    # ===== Add a new task =====
    elif menu == 'a':
        # get passwords again in case we have added a new user in the meantime
        passwords = get_passwords()
        valid_username = False
        while not valid_username:
            # useful to be able to get a list of users so you don't have to
            # remember their username
            task_user = input("\nPlease enter a username to create a new \
task for them. (Enter 'l' to get a list of usernames): ").strip().lower()
            if task_user == 'l':
                for user in passwords.keys():
                    print(user)
            elif task_user == 'e':
                print("\nExiting")
                exit()
            elif task_user not in passwords.keys():
                print("\nError. User not found.")
            else:
                valid_username = True

        title = ''
        valid_title = False
        while not valid_title:
            title = input("\nPlease enter a title for the task: ").strip()
            if len(title) < 0:
                print("\nError. Nothing entered.")
            elif title == 'e':
                print("\nExiting")
                exit()
            else:
                valid_title = True

        description = ''
        valid_description = False
        while not valid_description:
            description = input(
                "\nPlease enter a description for the task: ").strip()
            if len(description) < 0:
                print("\nError. Nothing entered.")
            elif description == 'e':
                print("\nExiting")
                exit()
            else:
                valid_description = True

        due_date = ''
        valid_date = False
        # use datetime module for getting and validating dates
        # https://www.w3schools.com/python/python_datetime.asp
        while not valid_date:
            due_date = input("\nPlease enter a due date in the following \
format 'yyyy-mm-dd' e.g. 2022-11-08: ").strip()
            if due_date == 'e':
                print("\nExiting")
                exit()
            # we use a try / except block to check that the user has entered
            # a valid date. We could use a stack of if statements here but
            # this is quicker
            try:
                due_date = datetime.date.fromisoformat(due_date)
                todays_date = datetime.date.today()
                # make sure our user isn't a time traveller!
                if todays_date > due_date:
                    print("\nDue date must be in the future.")
                else:
                    # convert dates to same format as existing ones
                    due_date = due_date.strftime("%d %b %Y")
                    todays_date = todays_date.strftime("%d %b %Y")
                    valid_date = True
            except ValueError:
                print("\nInvalid date format.")

        # construct our task string
        line = '\n' + ', '.join([task_user, title,
                                description, todays_date, due_date, "No"])

        # append our task to file on a new line
        with open(tasks_path, 'a') as f:
            f.write(line)

        print(f"""\nNew task added for {task_user}""")

    # ===== Display all tasks =====
    elif menu == 'va':
        all_tasks = []
        with open(tasks_path, 'r') as f:
            for line in f:
                # split our task up
                line = line.split(', ')
                # construct a seperator for formatting
                seperator = '_' * 80

                # The task description has the output looking like the below:
                # _____________________________________________________________________________

                # Task:                   Register Users with taskManager.py
                # Assigned to:            admin
                # Date assigned:          10 Oct 2019
                # Due date:               20 Oct 2019
                # Task Complete?          No
                # Task Description:
                #  Use taskManager.py to add the usernames and passwords for all team members that will be using this program.
                # _____________________________________________________________________________

                # However it would be good to have the task description wrap
                # and be aligned with the other iems so let's do that.
                # After we've entered the title on each line we only have 56
                # characters to play with and the description may be longer
                # than this, so we want to split it up and print it on seperate
                # lines
                desc_first_line = ''
                desc = line[2].strip()
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
Task:                   {line[1].strip()}
Assigned to:            {line[0].strip()}
Date assigned:          {line[3].strip()}
Due date:               {line[4].strip()}
Task Complete?          {line[5].strip()}
Task Description:       {desc_first_line}""")

                for desc_line in desc_lines:
                    print(" " * 24 + desc_line)
                print(seperator)

    # ===== Display tasks for logged in user =====
    elif menu == 'vm':
        user_tasks = []
        with open(tasks_path, 'r') as f:
            # we want to print a message if our user has no tasks
            has_tasks = False
            for line in f:
                # split our task up
                line = line.split(', ')
                if line[0] == logged_in_user:

                    if has_tasks is False:
                        print(f"""\nTasks for {logged_in_user}:""")

                    has_tasks = True
                    desc_first_line = ''
                    desc = line[2].strip()
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
Task:                   {line[1].strip()}
Assigned to:            {line[0].strip()}
Date assigned:          {line[3].strip()}
Due date:               {line[4].strip()}
Task Complete?          {line[5].strip()}
Task Description:       {desc_first_line}""")

                    for desc_line in desc_lines:
                        print(" " * 24 + desc_line)
                    print(seperator)
            if not has_tasks:
                print(f"""\nSorry {logged_in_user} You have no tasks.""")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
