"""An implementation of a stock keeping system with a sqlite3 backend."""
import sqlite3
import os
import sys
from tabulate import tabulate
# Throughout this exercise the connection object is used as a context manager
# when changes are made to the db to prevent having to manually commit or
# rollback when a transaction fails.
# See https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'data', 'bookstore')

# define some aliases. Do this rather than using import from so we also have
# access to exceptions etc.
Cursor = sqlite3.Cursor
Connection = sqlite3.Connection
connect = sqlite3.connect


def main():
    """Run the main loop."""
    # Wrap everything in a try / except / finally clause to ensure we always
    # close db connection
    try:
        conn = connect(db_path)
        create_table(conn)
        populate_table(conn)
        main_menu(conn)
    except sqlite3.Error as err:
        print(err)
    finally:
        conn.close()


def main_menu(conn: Connection):
    """Display Main Menu.

    Arguments:
        conn -- bookstore db connection.
    """
    try:
        while True:
            results = get_all_books(conn)
            headers = get_headers(results)
            rows = results.fetchall()
            print_table(headers, rows)
            option = input(
                """Please select from the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
:""").strip().lower()
            match option:
                case '1':
                    enter_book(conn)
                case '2':
                    update_book(conn)
                case '3':
                    delete_book(conn)
                case '4':
                    search_books_menu(conn)
                case '0':
                    print("Exiting")
                    sys.exit()
                case _:
                    print("Invalid Input")
    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def create_table(conn: Connection):
    """Create table.

    Arguments:
        conn -- bookstore db connection

    Raises:
        Exception: sqlite3 error
    """
    try:
        with conn:
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS
                    books(
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    qty INTEGER)''')
    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def populate_table(conn: Connection):
    """Populate books table with initial values.

    Arguments:
        conn -- bookstore db connection

    Raises:
        sqlite3.Error: sqlite3 error
    """
    books = [
        (3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
        (3005, "Alice in Wonderland", "Lewis Carroll", 12)
    ]
    try:
        with conn:
            conn.executemany(
                """INSERT OR IGNORE INTO books(id, title, author, qty)
                VALUES(?, ?, ?, ?)""", books)
    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def get_headers(results: Cursor) -> list:
    """Return column headers.

    Use this and call it in pretty print functions so if we choose to add or
    remove columns to our table at some point in future we don't need to
    alter these functions.

    Arguments:
        results -- Cursor with results

    Returns:
        list of column headers
    """
    return [x[0] for x in results.description]


def get_all_books(conn: Connection) -> Cursor:
    """Return all books.

    Arguments:
        conn -- bookstore db connection

    Raises:
        sqlite3.Error: sqlite error

    Returns:
        sqlite3 cursor containing all books
    """
    try:
        results = conn.execute("SELECT * FROM books")
        return results
    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def delete_book(conn: Connection):
    """Delete a book from the database.

    Arguments:
        conn -- bookstore db connection

    Raises:
        sqlite3.Error: sqlite3 error
    """
    while True:
        id = get_book_id()
        if id is False:
            return
        try:
            results = conn.execute(
                """SELECT * FROM books WHERE id = ?""", (id,))
            data = results.fetchone()
            if data is None:
                print("No book with that id")
                continue
            else:
                print("Deleting the following book:")
                results = conn.execute(
                    """SELECT * FROM books WHERE id = ?""", (id,))
                print_results(results)
                with conn:
                    conn.execute("""DELETE FROM books WHERE id = ?""", (id,))
            while True:
                option = input(
                    "Would you like to delete another book? (y/n): "
                ).strip().lower()
                if option == 'y':
                    break
                elif option == 'n':
                    return
                else:
                    print("Error. Invalid option. Please Enter 'y' or 'n'")
        except sqlite3.Error as err:
            raise sqlite3.Error(err)


def print_table(headers: list, rows: list):
    """Pretty print a table of results.

    Arguments:
        headers -- Table headers
        row -- Table Rows
    """
    print(tabulate(rows, headers=headers,
          tablefmt="fancy_grid", numalign="center"))


def enter_book(conn: Connection):
    """Allow user to enter details of book to add to database.

    Arguments:
        conn -- bookstore db connection

    Raises:
        sqlite3.Error: sqlite3 error.
    """
    title = ''
    author = ''
    qty = None
    while True:
        # perform this check so if user enters an invalid input for author
        # they don't have to re-enter title etc.
        if not title:
            title = input("Book Title: ").strip()
            if not title:
                print("Invalid Input. Please enter a title.")
                continue
        if not author:
            author = input("Author: ").strip()
            if not author:
                print("Invalid Input. Please enter an author.")
                continue
        if not qty:
            qty = input("Quantity: ").strip()
            if not qty:
                print("Invalid input. Cannot be blank or zero.")
                continue
            try:
                qty = int(qty)
            except ValueError:
                qty = None
                print("Invalid Input. Must be a number.")
                continue
        try:
            result = insert_book(conn, (title, author, qty))
            print("\nNew book created:")
            print_results(result)
            title = author = qty = None
            while True:
                result = input("Enter another? (y/n)\n:").strip().lower()
                if result == 'y':
                    break
                elif result == 'n':
                    main_menu(conn)
                else:
                    print("Invalid Input")
                    continue
        except sqlite3.Error as err:
            raise sqlite3.Error(err)


def insert_book(conn: Connection, book: tuple[str, str, int]) -> Cursor:
    """Insert new book into database and return it.

    Arguments:
        conn -- bookstore db connection
        book -- title, author, qty

    Raises:
        sqlite3.Error: sqlite3 error

    Returns:
        Cursor pointing to new row
    """
    try:
        with conn:
            cursor = conn.execute(
                """INSERT INTO books(title, author, qty)
                VALUES(?, ?, ?)""", book)
        results = conn.execute(
            "SELECT * FROM books WHERE id = ?", (cursor.lastrowid,))
        return results
    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def get_book_by_id(conn: Connection, id: int) -> Cursor:
    """Return book by id.

    Arguments:
        conn -- bookstore db connection
        id -- book id

    Raises:
        sqlite3.Error: sqlite3 error

    Returns:
        Cursor pointing to book
    """
    try:
        results = conn.execute(
            "SELECT * FROM books WHERE id = ?", (id,))
        return results
    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def update_book(conn: Connection):
    """Ask user to select a book to update and then update it.

    Arguments:
        conn -- bookstore db connection
    """
    while True:
        book_id = get_book_id()
        if book_id:
            book = get_book_by_id(conn, book_id)
            headers = get_headers(book)
            rows = book.fetchall()
            if rows:
                print_table(headers, rows)
                update_book_menu(conn, book_id)
            else:
                print("\nError. Book not found\n")
        else:
            return


def update_title(conn: Connection, book_id: int):
    """Update title of book.

    Arguments:
        conn -- bookstore db connection
        book_id -- book id
    """
    title = input("Please enter new title: ")
    with conn:
        conn.execute(
            """UPDATE books
            SET title = ?
            WHERE id = ?""", (title, book_id))


def update_author(conn: Connection, book_id: int):
    """Update author of book.

    Arguments:
        conn -- bookstor db connection
        book_id -- book id
    """
    author = input("Please enter new author: ")
    with conn:
        conn.execute(
            """UPDATE books
            SET author = ?
            WHERE id = ?""", (author, book_id))


def update_qty(conn: Connection, book_id: int):
    """Update quantity of book.

    Arguments:
        conn -- bookstore db connection
        book_id -- book id
    """
    qty = input("Please enter new quantity: ")
    with conn:
        conn.execute(
            """UPDATE books
            SET qty = ?
            WHERE id = ?""", (qty, book_id))


def update_book_menu(conn: Connection, book_id: int):
    """Print menu for user to update book details.

    Arguments:
        conn -- bookstore db connection
        book_id -- book id
    """
    try:
        while True:
            option = input("""What would you like to do with the book?
1.  Edit Title
2.  Edit Author
3.  Edit Quantity
-1. Back
0.  Exit
: """).strip()
            match option:
                case '1':
                    update_title(conn, book_id)
                case '2':
                    update_author(conn, book_id)
                case '3':
                    update_qty(conn, book_id)
                case '-1':
                    return
                case '0':
                    print("Exiting")
                    sys.exit()
                case _:
                    print("\nInvalid input.\n")
                    continue
            if option in ['1', '2', '3']:
                print("\nBook Updated\n")
                results = conn.execute(
                    """SELECT * FROM books
                    WHERE id = ?""", (book_id,)
                )
                print_results(results)

    except sqlite3.Error as err:
        raise sqlite3.Error(err)


def get_book_id() -> int:
    """Get book id from user input and check it is in valid format.

    Returns:
        book id
    """
    while True:
        book_id = input(
            """Please enter a book ID
0.  Exit
-1. Back
: """).strip().lower()
        try:
            book_id = int(book_id)
            match book_id:
                case -1:
                    return
                case 0:
                    print("\nExiting\n")
                    sys.exit()
            return book_id
        except ValueError:
            print("Invalid input")
            continue


def search_books_menu(conn):
    """Print menu allowing user to perfrom a general or more specific search.

    Arguments:
        conn -- bookstore db connection
    """
    while True:
        option = input(
            """
Please enter your search term to search by ID, Author or Title
or choose from the following options to narrow your search:
1.  Search by ID
2.  Search by Author
3.  Search by Title
4.  Search by Quantity
0.  Exit
-1. Back
: """).strip().upper()
        match option:
            case '1':
                search_by_id(conn)
            case '2':
                search_by_author(conn)
            case '3':
                search_by_title(conn)
            case '4':
                search_by_qty(conn)
            case '0':
                print("Exiting.")
                sys.exit()
            case '-1':
                return
            case '':
                print("Error. Nothing Entered.")
            case _:
                search_all(conn, option)


def search_by_qty(conn: Connection):
    """Allow user to search for book by quantity of stock.

    Can also be used to get the details of the SKU with the largest or
    smallest quantity of stock.

    Arguments:
        conn -- bookstore db connection
    """
    # use back and exit instead of 0 and -1 in case user wants to get books
    # with 0 stock remaining
    query = input(
        """Please enter a number to return a list of books with that amount
of stock or choose from the following options:
max - returns details of the SKU with the greatest level of stock
min - returns the SKU with the least amount of stock
back - return to previous menu
exit - exit program
: """
    ).strip().lower()

    try:
        query = int(query)
        results = conn.execute(
            """SELECT * FROM books
            WHERE qty = ?""", (query,))
        print_results(results)
    except ValueError:
        match query:
            case 'max':
                result = conn.execute(
                    """SELECT * FROM books
                    WHERE qty = (SELECT MAX(qty) FROM books)""")
                print_results(result)
            case 'min':
                result = conn.execute(
                    """SELECT * FROM books
                    WHERE qty = (SELECT MIN(qty) FROM books)""")
                print_results(result)
            case 'back':
                return
            case 'exit':
                print("Exiting")
                sys.exit()
            case _:
                print("\nError. Invalid Input\n")


def print_results(
        results: Cursor,
        message="\nNo Results Found\n"):
    r"""Pretty print results as table.

    Arguments:
        results -- Cursor containing results

    Keyword Arguments:
        message -- Message to display if there are no results
        (default: {"\nNo Results Found\n"})
    """
    headers = get_headers(results)
    # We perform this step so we can check whether there are any rows as the
    # .countrows methods isn't reliable for all queries
    rows = results.fetchall()
    if rows:
        print_table(headers, rows)
    else:
        print(message)


def search_by_author(conn: Connection):
    """Allow user to search by author and print results.

    Arguments:
        conn -- bookstore db connection
    """
    search_str = input("Please enter search term: ").strip().upper()
    search_str = '%' + search_str + '%'
    results = conn.execute(
        """SELECT * FROM books
        WHERE author LIKE ? COLLATE NOCASE""",
        (search_str,))
    print_results(results)


def search_by_title(conn: Connection):
    """Allow user to search by title and print results.

    Arguments:
        conn -- bookstore db connection
    """
    search_str = input("Please enter search term: ").strip().upper()
    search_str = '%' + search_str + '%'
    results = conn.execute(
        """SELECT * FROM books
        WHERE title LIKE ? COLLATE NOCASE""",
        (search_str,))
    print_results(results)


def search_by_id(conn: Connection):
    """Allow user to search by id and print results.

    Arguments:
        conn -- bookstore db connection
    """
    while True:
        id = get_book_id()
        if id:
            results = get_book_by_id(conn, id)
            print_results(results)
        else:
            return


def search_all(conn: Connection, search_str: str):
    """Search in id, author and title columns and print results.

    Arguments:
        conn -- bookstore db connection
        search_str -- search string
    """
    search_str = "%" + search_str + "%"
    results = conn.execute(
        """SELECT * FROM books
        WHERE id LIKE ?
        OR author LIKE ?
        OR title LIKE ? COLLATE NOCASE""",
        (search_str, search_str, search_str))
    print_results(results)


if __name__ == "__main__":
    main()
