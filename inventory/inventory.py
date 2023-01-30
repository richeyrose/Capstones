"""This module defines a shoe inventory systemt hat can be interacted with."""
import csv
import os
from tabulate.tabulate import tabulate
#from __future__ import annotations

# Note on original submision:
# The "TypeError: 'type' object is not subscriptable" that I was marked down on
# is due to the script being run in a pre-3.90 version of python.
# Uncommenting from __future__ import annotations should fix this error for
# this file as long as you are using 3.70 or above.
# I've spoken to Leon Stevens about this and he has assured me that all
# assessors have now updated to version 3.10 so we can use modern features
# such as subscriptable type annotations and match / case statements.
# However it does not appear that the original assessor of this assignment had
# got the message prior to the original submission.
# If you are still getting this error please can you ensure you are using
# python 3.10 as I have been told this is the version all assessors should be
# using

# Comments:
# [1] Because I can't guarantee that the assessor will have tabulate installed
# I've packaged it up in the directory and imported it.

# [2]In one of my previous assginments I got the comment that using the -> None
# type annotations for functions and methods that return none was redundant.
# However since it is in the PEP-484 spec for type hinting and is useful for
# seeing the return type in the IDE and testing I'm going to keep on
# using it.
# e.g. see the examples at :
# https://peps.python.org/pep-0484/#instantiating-generic-classes-and-type-erasure


# References
# [1] Phlips, D. (2018) Python 3 Object-Oriented Programming, 3rd ed. Packt
# [2] https://realpython.com/
# [3] https://www.python.org/
# ========The beginning of the class==========


class Shoe:
    """Represents a shoe in a warehouse inventory system.

    Attributes:
        country -- Country of origin
        code -- Code in form of SKU12345
        product -- Shoe name
        cost -- Cost of individual SKU
        quantity -- Units of stock of SKU
    """

    def __init__(
            self,
            country: str,
            code: str,
            product: str,
            cost: float,
            quantity: int) -> None:
        """Init Shoe with country, code, product, cost and quantity."""
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self) -> float:
        """Return cost of individual unit of Shoe.

        Returns:
            cost of Shoe.
        """
        return self.cost

    def get_quantity(self) -> int:
        """Return quantity of stock of Shoe.

        Returns:
            Quantity of Shoe in warehouse
        """
        return self.quantity

    def get_product(self) -> str:
        """Return product name of Shoe.

        Returns:
            Shoe name
        """
        return self.product

    def get_country(self) -> str:
        """Return Country of origin.

        Return:
            Country of origin.
        """
        return self.country

    def get_code(self) -> str:
        """Return SKU code.

        Returns:
            Code in form SKU12345.
        """
        return self.code

    def restock(self, qty) -> int:
        """Restock the shoe by adding the passed in quantity.

        Arguments:
            qty -- Quantity to add to existing stock

        Returns:
            New quantity of stock
        """
        self.quantity = self.quantity + qty
        return self.quantity

    def __str__(self) -> str:
        """Return formatted representation of Shoe.

        Returns:
            string in form:
            '
             product:   A Shoe
             code:      SKU12345
             country:   UK
             cost:      100
             quantity:  50'
        """
        return f"""
    product:  {self.product}
    code:     {self.code}
    country:  {self.country}
    cost:     {self.cost}
    quantity: {self.quantity}"""

    def __repr__(self) -> str:
        """Return representation of shoe that can be fed to eval().

        Returns:
            string in form:
            Shoe(
                country='UK',
                code='SKU12345',
                product='A Shoe'
                cost=100
                quantity=200)
        """
        return f"""Shoe(
            country={self.country},
            code={self.code},
            product={self.product},
            cost={self.cost},
            quantity={self.quantity})"""


# =============Shoe list===========
# The list will be used to store a list of objects of shoes.
# Ooh we can use annotations on variables as well! Probably less useful
# a lot of the time but could have it's uses
shoe_list: list[Shoe] = []

# ensure we can get path to inventry.txt even if user is in different directory
# when they execute script
current_dir = os.path.dirname(os.path.abspath(__file__))
inventory_path = os.path.join(current_dir, 'inventory.txt')


# ==========Functions outside the class==============
def read_shoes_data():
    """Read shoe data from inventory.txt and append to shoes."""
    try:
        with open(inventory_path, 'r', encoding='utf-8') as file:
            # using the DictReader method in the csv module allows
            # us to create a dict from each line of the file.
            # Not specifying a fieldnames property uses the first line as the
            # dictionary key
            # https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                shoe_list.append(
                    Shoe(row['Country'],
                         row['Code'],
                         row['Product'],
                         row['Cost'],
                         row['Quantity']))
    except FileNotFoundError:
        print("Could not find inventory.txt")


def check_generic_option(option: str, is_num: bool = False) -> None | bool:
    """Handle generic options entered by user.

    Handles blank, back and exit options in a consistent way. Also checks
    that the user has entered a valid number if is_num is True

    Arguments:
        option -- option entered by user. 'b', 'e', or string rep resentation
        of number

    Keyword Arguments:
        is_num -- Whether to check if option is a valid number

    Raises:
        ValueError: If the user has entered an invalid number and is_num
        is True a ValueError will be raised.

    Returns:
        True if user has entered nothing or invalid input.
    """
    if option == '':
        print("Error. Nothing entered.")
        return True
    elif option == 'b':
        main_menu()
    elif option == 'e':
        print("Goodbye")
        exit()
    elif is_num:
        try:
            option = float(option)
            return False
        except ValueError('Error. Not a number') as error:
            raise ValueError from error


def capture_shoes() -> None:
    """Create a Shoe object from user input.

    Capture data about a shoe from user input and use this data to create a
    shoe object and append this object to shoe_list.
    """
    # Put our intial print statement outside the while loop so we show
    # an altered one after it has run at least once.
    initial_menu = """
Please enter the details of the shoe
or choose from the following options.
b - back
e - exit
"""

    # altered statement
    looped_menu = """
To add another shoe please enter its details
or choose from the following options.
b - back
e - exit
"""
    menu = initial_menu
    while True:
        product = ''
        code = ''
        country = ''
        cost = ''
        quantity = ''
        print(menu)
        try:
            # break these out into seperate functions so we don't end up
            # with a hard to read stack of while loops
            product = enter_product()
            code = enter_code()
            country = enter_country()
            cost = enter_cost()
            quantity = enter_quantity()
        except ValueError as error:
            print(error)
            menu = (looped_menu)
            continue

        # append new shoe to file
        new_shoe = Shoe(country, code, product, cost, quantity)
        append_shoe_data([country, code, product, cost, quantity])

        # update shoe list
        shoe_list.append(new_shoe)
        print(f"""
New shoe added: {new_shoe}""")
        menu = looped_menu


def enter_product() -> str:
    """Get name of new product from user.

    Checks that product with that name doesn't alread exist.

    Returns:
        product name
    """
    while True:
        product = input("""Name of the shoe: """).strip()
        shoes = get_shoe_list()
        if product == '':
            print("Error. Nothing entered.")
            continue
        shoes = [x.get_product().lower() for x in shoes]
        if product.lower() in shoes:
            print(
                """
Error. Product with that name already exists.
Please enter a unique name
""")
            continue
        elif check_generic_option(product):
            continue
        else:
            return product


def enter_code() -> str:
    """Return new SKU from user.

    Validates SKU and checks that it is unique

    Returns:
        valid SKU
    """
    while True:
        code = input(
            """Please enter a product code of the form SKU12344 \
or 12345: """).strip().lower()
        if code == '':
            print("Error. Nothing entered.")
            continue
        elif check_generic_option(code):
            continue
        else:
            code = validate_sku(code)
            existing_codes = [x.get_code() for x in shoe_list]
            if code not in existing_codes:
                return code
            else:
                print("Error. Code already exists.")


def enter_country() -> str:
    """Return country of origin from user input.

    Returns:
        Country of origin
    """
    while True:
        country = input(
            """Please enter the country of origin: """)
        if country == '':
            print("Error. Nothing entered.")
            continue
        elif check_generic_option(country):
            continue
        else:
            return country


def enter_cost() -> float:
    """Return cost as float from user input.

    Raises:
        ValueError: Error if user doesn't enter a valid number

    Returns:
        cost of product
    """
    while True:
        try:
            cost = input("""Unit cost: """).strip()
            # format float to have trailing zeros: 1234.00
            if cost == '':
                print("Error. Nothing entered.")
                continue
            elif check_generic_option(cost, is_num=True):
                continue
            else:
                cost = round(float(cost), 2)
                return cost
        except ValueError:
            raise ValueError


def enter_quantity() -> int:
    """Return quantity of product from user input.

    Raises:
        ValueError: Error if user enters non number

    Returns:
        quantity of product entered.
    """
    while True:
        try:
            quantity = input(
                """Please enter the quantity: """).strip()
            if quantity == '':
                print("Error. Nothing emtered.")
                continue
            elif check_generic_option(quantity, is_num=True):
                continue
            else:
                quantity = int(quantity)
                return quantity
        except ValueError('Error. Not a number') as error:
            raise ValueError from error


def append_shoe_data(shoe_data: list) -> None:
    """Write a new row to the inventory file.

    Arguments:
        shoe_data -- list representation of shoe.
    """
    with open(inventory_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows([shoe_data])


def view_all() -> None:
    """Iterate over shoe list and print details of shoes using tabulate."""
    shoes = get_shoe_details(shoe_list)
    # format cost as currency
    for shoe in shoes:
        shoe[3] = f"R{shoe[3]:.2f}"

    print(tabulate(shoes,
                   headers=["Index", "Country",
                            "Code", "Product", "Cost", "Quantity"],
                   showindex='always',
                   tablefmt='fancy_grid'))


def get_shoe_details(shoes) -> list[list]:
    """Return a list of the details of all shoes passed in.

    Returns:
        list of Country,Code,Product,Cost,Quantity for all shoes passed in
    """
    # methods to use in a list comprehension to get details of shoe.
    # This is probably over engineered but wanted to try it.
    country = Shoe.get_country
    product = Shoe.get_product
    qty = Shoe.get_quantity
    cost = Shoe.get_cost
    code = Shoe.get_code
    shoes = [[country(x), code(x), product(x), cost(x), qty(x)]
             for x in shoes]
    return shoes


def write_shoes_data():
    """Write shoe_list to inventory.txt."""
    shoe_details = get_shoe_details(shoe_list)
    with open(inventory_path, 'w', encoding='utf-8', newline='') as file:
        headers = ["Country", "Code", "Product", "Cost", "Quantity"]
        writer = csv.writer(file, delimiter=',')
        writer.writerow(headers)
        writer.writerows(shoe_details)


def re_stock():
    """Find shoe object with lowest quantity and give option to restock.

    updates inventory.txt
    """
    while True:
        # sort list using quantity as key to get shoe with lowest quantity of
        # stock
        sorted_list = sorted(
            shoe_list,
            key=lambda x: x.get_quantity())

        # Get shoe with lowest stock and check user hasn't deleted all
        # the shoes (I did this in testing. Oops)
        try:
            shoe = sorted_list[0]
        except IndexError:
            print("Error. No shoes found!")
            return False

        # get name of shoe and stock level
        product = shoe.get_product()
        current_stock = shoe.get_quantity()

        # Get user option
        option = input(f"""
The stock of {product} is running low.
There are only {current_stock} units left.
Would you like to restock?
y - yes
n - no
b - back
e - exit
: """).strip().lower()

        if option == 'n':
            print("Returning to main menu.")
            main_menu()
        elif option == 'y':
            try:
                qty = int(input("""
How many units would you like to order?
: """).strip())
            except ValueError("Error. Not a number") as error:
                print(error)
                continue
            else:
                # use restock method added to our shoe
                restocked_qty = shoe.restock(qty)
                # update file
                write_shoes_data()

                print(f"""
{qty} units of {product} added.

There are now {restocked_qty} in stock.
""")
            if restock_more_menu():
                continue


def restock_more_menu() -> bool | None:
    """Menu that asks user if they want to restock another shoe or back out.

    Returns:
        True if the user answers yes.
    """
    while True:
        restock_more = input(
            """Would you like to restock the next shoe?
y - yes
n - no
b - back
e - exit
: """).strip().lower()
        if restock_more == '':
            print("Error. Nothing entered")
            continue
        elif restock_more == 'y':
            return True
        elif restock_more == 'n':
            print("Returning to main menu.")
            main_menu()
        elif check_generic_option(restock_more):
            continue


def search_shoe(code: str) -> Shoe | bool:  # corrected spelling to search_shoe
    """Return a shoe from shoe_list if it exists.

    Arguments:
        code -- shoe code

    Returns:
        Shoe
    """
    for shoe in shoe_list:
        shoe_code = shoe.get_code()
        if shoe_code == code:
            return shoe
    return False


def search_shoe_menu() -> None:
    """Display a menu that allows user to search for a shoe by SKU number."""
    SKUs = [x.get_code() for x in shoe_list]

    while True:
        option = input("""
Please enter the SKU for the shoe or enter one of
the following options:
v - view all shoes
b - back
e - exit
: """).lower().strip()
        if option == '':
            print("Error. Nothing entered.")
            continue
        elif option == 'v':
            view_all()
        sku = validate_sku(option)
        if sku in SKUs:
            shoe = search_shoe(sku)
            if shoe:
                print(shoe)
        elif check_generic_option(option):
            continue
        else:
            print("No shoe found with that SKU.")
            continue


# using a getter function with type annotations
# makes the linter and autocomplete work better


def get_shoe_list() -> list[Shoe]:
    """Return the shoe list.

    using a getter function with type annotations
    makes the linter and autocomplete work better
    """
    return shoe_list


def value_per_item_menu():
    """Display menu with options for using value per item table."""
    # Menu loop
    while True:
        option = input("""
To view details of a shoe please enter the product code or
select from the following options:
t - list total value of shoes
b - back
e - exit
: """).strip().lower()
        if option == '':
            print("Error. Nothing entered.")
            continue
        # allow user to redisplay menu
        elif option == 't':
            value_per_item()
        # check that user has entered a valid SKU number. They can either
        # include the SKU or not
        sku = validate_sku(option)
        if sku:
            # get shoe and print
            shoe = search_shoe(sku)
            if shoe:
                print(shoe)
            else:
                print("No shoe found with that SKU")
                continue
        else:
            check_generic_option(option)
            continue


def validate_sku(sku: str) -> str:
    """Check whether SKU is in correct format.

    Arguments:
        sku -- string in formnat SKU12345

    Returns:
        string in format SKU12345 or False
    """
    # strip 'sku' character from front of string (if present) and
    # check that rest of characters are numeric and there are 5 of them
    sku = sku.lower().strip()
    number_check = sku.replace('sku', '')
    if number_check.isnumeric() \
            and len(number_check) == 5:
        sku = f"SKU{number_check}"
        return sku
    return False


def value_per_item():
    """Print the total value of stock held for each shoe.

    Allows the user to view the details of a shoe or refresh table.
    """
    product = Shoe.get_product
    qty = Shoe.get_quantity
    cost = Shoe.get_cost
    code = Shoe.get_code
    shoes = [[code(x), product(x), qty(x) * cost(x)]
             for x in shoe_list]

    # Sum the cost of our shoes so we can get the total value of our stock
    total = sum([x[-1] for x in shoes])

    # display costs and format as currency
    for shoe in shoes:
        shoe[-1] = f"R{shoe[-1]:.2f}"
    shoes.append([" ", "Total", f"R{total:.2f}"])

    # Use tabulate module to present results
    print("\nTotal Value of shoes:")
    headers = ["Code", "Product", "Total Value"]

    print(tabulate(shoes,
                   headers=headers,
                   tablefmt='fancy_grid',
                   numalign="center"))

    # print menu to allow user to interact with list
    value_per_item_menu()


def highest_qty() -> None:
    """Print the shoe which is currently on sale.

    This is the shoe with the highest quantity of stock.
    """
    # sort list using quantity as key and reverse it
    sorted_list = sorted(
        shoe_list,
        key=lambda x: x.get_quantity(),
        reverse=True)

    print(f"""
    Now on Sale!
    {sorted_list[0]}""")


# ==========Main Menu=============
def main_menu() -> None:
    """Display the main menu to user."""
    while True:
        option = input("""
Please choose from the following options:
v - view all
a - add new shoe
s - search for shoe
r - restock shoe
g - get shoe that is on sale
t - list total value of shoes
e - exit
: """).strip().lower()
        if option == 'v':
            view_all()
        elif option == 'a':
            capture_shoes()
        elif option == 's':
            search_shoe_menu()
        elif option == 'r':
            re_stock()
        elif option == 'g':
            highest_qty()
        elif option == 't':
            value_per_item()
        elif option == 'e':
            print("Goodbye.")
            exit()
        else:
            print("Error. Invalid input.")


def main():
    """Execute program to display and add to shoe inventory."""
    read_shoes_data()
    main_menu()


if __name__ == "__main__":
    main()
