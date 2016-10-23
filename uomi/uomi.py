#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
import os
import argparse
import textwrap
parser = argparse.ArgumentParser(description='A tool to manage debts and credits owed.\
                                             The default behaviour is to list everything.')
parser.add_argument('-ad', '--add-debt',
                    help='Add debt',
                    action='store_const',
                    const='+D',
                    dest='type')
parser.add_argument('-ac', '--add-credit',
                    help='Add credit',
                    action='store_const',
                    const='+C',
                    dest='type')
parser.add_argument('-dd', '--delete-debt',
                    help='Add debt',
                    action='store_const',
                    const='-D',
                    dest='type')
parser.add_argument('-dc', '--delete-credit',
                    help='Add credit',
                    action='store_const',
                    const='-C',
                    dest='type')

args = parser.parse_args()


def main():
    """Main is here so I can hide long ugly lists of SQL variables at the bottom."""
    os.system('clear')
    print('\nUoMi\n')
    try:
        cnx = mysql.connector.connect(user='uomi',
                                      password='B9cSPPc73AKUSuX6',
                                      host='kibostor')
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print(err)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password,\n"
                  "or you don't have permission to that db.")
        else:
            print("Some other error has occured")
            print(err)
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Call Make DB\n")
            create_database(cursor)
            cnx.database = DB_NAME
            print("Call Make Tables\n")
            create_tables(cursor)
        else:
            print(err)
            exit(1)

    if args.type:
        print(args.type)
        print("type")
        if args.type == "+D":
            add_debt(cursor)
            cnx.commit()
            print_debt(cursor)

        elif args.type == "+C":
            add_credit(cursor)
            print_credit(cursor)
            cnx.commit()
        elif args.type == "-D":
            delete_debt(cursor, cnx)
            print_debt(cursor)
            cnx.commit()
        elif args.type == "-C":
            delete_credit(cursor, cnx)
            print_credit(cursor)
            cnx.commit()

    else:

        print_debt(cursor)
        print("\n"*4)
        print_credit(cursor)


def create_database(in_cursor):
    """Create the database under this user if it cannot be found."""
    try:
        in_cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    else:
        print("DB Created")


def create_tables(in_cursor):
    """Create tables in database."""
    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            in_cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("Tables Created")


def add_debt(in_cursor):
    """Insert a debt I owe into the database."""
    os.system('clear')
    print("Add Debt\n")
    person = input('Enter name:\n')
    cbo = ""
    while True:
        cbo = input('(c)ash, (b)arter, (o)ther:\n')
        if cbo in ['c', 'b', 'o']:
            break
    amount = int(input("Cash:\n$") or "0")
    barter = input("Barter:\n") or ""
    other = input("Other:\n") or ""
    debt = "INSERT INTO debt (date, name, type, value, barter, other, pay_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    print(debt)
    payback = datetime.now().date() + timedelta(seconds=160000 + (((amount ** 0.5) * 1.5) * 90000))
    today = datetime.now().date()
    debt_data = (today, person, cbo, amount, barter, other, payback)
    in_cursor.execute(debt, debt_data)
    print(in_cursor.lastrowid)


def delete_debt(in_cursor, cnx):
    recd = input('Which Record?\n')
    delete = "DELETE FROM debt WHERE debt_no = %s"
    delete_data = (recd,)
    print(delete, delete_data)
    in_cursor.execute(delete, delete_data)
    cnx.commit()


def print_debt(in_cursor):
    """Print all the debts I owe"""
    query = "SELECT `debt_no`, `date`, `name`, `type`, `value`, `barter`, `other`, `pay_date` FROM `debt` WHERE 1"
    in_cursor.execute(query)
    total = 0
    row = 0
    print("Debts\n")
    for rec in in_cursor:
        total += int(rec[4])
        r = [str(rec[i]) for i in range(0, 8)]  # Reordering the record too.
        if row == 0:
            print_table(
                [[r[0].zfill(3), r[1], r[7], r[2], r[4], r[5], r[6]], ],
                header=["#", "Date", "Paydate", "Name", "Cash", "Barter", "Other"],
                wrap=True, max_col_width=14, wrap_style='wrap',
                row_line=False, fix_col_width=True)
            row = 1
        else:
            print_table(
                [[r[0].zfill(3), r[1], r[7], r[2], r[4], r[5], r[6]], ],
                wrap=True, max_col_width=14, wrap_style='wrap',
                row_line=False, fix_col_width=True)
    print("Cash $" + str(total), "\n")

def add_credit(in_cursor):
    """Insert a credit I am owed into the database.
    Repay time is calculated as slightly less than two days (160ksec)
    plus a little over a day (90ksec) for every $13 or so on a sliding scale.
    (I enjoy decimal-second timekeeping. sue me.)
    """
    person = input('Enter name:\n')
    cbo = ""
    while True:
        cbo = input('(c)ash, (b)arter, (o)ther:\n')
        if cbo in ['c', 'b', 'o']:
            break
    amount = int(input("Cash:\n$") or "0")
    barter = input("Barter:\n")
    other = input("Other:\n")
    credit = "INSERT INTO credit (date, name, type, value, barter, other, pay_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    payback = datetime.now().date() + timedelta(seconds=160000 + (((amount ** 0.5) * 1.5) * 90000))
    today = datetime.now().date()
    credit_data = (today, person, cbo, amount, barter, other, payback)
    print(credit, "\n")
    print(credit_data)
    in_cursor.execute(credit, credit_data)
    print(in_cursor.lastrowid)


def delete_credit(in_cursor, cnx):
    recd = input('Which Record?\n')
    delete = "DELETE FROM credit WHERE credit_no = %s"
    delete_data = (recd,)
    print(delete, delete_data)
    in_cursor.execute(delete, delete_data)
    cnx.commit()


def print_credit(in_cursor):
    """Print all the credit owed me."""
    query = "SELECT `credit_no`, `date`, `name`, `type`, `value`, `barter`, `other`, `pay_date` FROM `credit` WHERE 1"
    in_cursor.execute(query)
    total = 0
    row = 0
    print("Credit\n")
    for rec in in_cursor:
        total += int(rec[4])
        r = [str(rec[i]) for i in range(0, 8)]  # Reordering the record too.
        if row == 0:
            print_table(
                [[r[0].zfill(3), r[1], r[7], r[2], r[4], r[5], r[6]], ],
                header=["#", "Date", "Paydate", "Name", "Cash", "Barter", "Other"],
                wrap=True, max_col_width=14, wrap_style='wrap',
                row_line=False, fix_col_width=True)
            row = 1
        else:
            print_table(
                [[r[0].zfill(3), r[1], r[7], r[2], r[4], r[5], r[6]], ],
                wrap=True, max_col_width=14, wrap_style='wrap',
                row_line=False, fix_col_width=True)

#        r = [str(rec[i]) for i in range(0, 8)]  # Reordering the record too.
#        print('{} {} {} {:12} ${:5} {:16} {:16} {}'.format(r[0], r[1], r[3], r[2], r[4], r[5], r[6], r[7]))
    print("Cash $" + str(total), "\n")


DB_NAME = 'uomi'
TABLES = {}
TABLES['debt'] = (
    "CREATE TABLE `debt` ("
    "  `debt_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `name` varchar(30) NOT NULL,"
    "  `type` enum('c','b','o') NOT NULL,"
    "  `value` int(11) NULL,"
    "  `barter` varchar(128) NULL,"
    "  `other` varchar(128) NULL,"
    "  `pay_date` date NOT NULL,"
    "  PRIMARY KEY (`debt_no`)"
    ") ENGINE=MyISAM")
TABLES['credit'] = (
    "CREATE TABLE `credit` ("
    "  `credit_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `name` varchar(30) NOT NULL,"
    "  `type` enum('c','b','o') NOT NULL,"
    "  `value` int(11) NULL,"
    "  `barter` varchar(128) NULL,"
    "  `other` varchar(128) NULL,"
    "  `pay_date` date NOT NULL,"
    "  PRIMARY KEY (`credit_no`)"
    ") ENGINE=MyISAM")


def print_table(items, header=None, wrap=True, max_col_width=20, wrap_style="wrap", row_line=False, fix_col_width=False):
    """ Prints a matrix of data as a human readable table. Matrix
    should be a list of lists containing any type of values that can
    be converted into text strings.

    Two different column adjustment methods are supported through
    the *wrap_style* argument:

       wrap: it will wrap values to fit max_col_width (by extending cell height)
       cut: it will strip values to max_col_width

    If the *wrap* argument is set to False, column widths are set to fit all
    values in each column.

    This code is free software. Updates can be found at
    https://gist.github.com/jhcepas/5884168

    """
    if fix_col_width:
        c2maxw = dict([(i, max_col_width) for i in range(len(items[0]))])
        wrap = True
    elif not wrap:
        c2maxw = dict([(i, max([len(str(e[i])) for e in items])) for i in range(len(items[0]))])
    else:
        c2maxw = dict([(i, min(max_col_width, max([len(str(e[i])) for e in items])))
                        for i in range(len(items[0]))])
    if header:
        current_item = -1
        row = header
        if wrap and not fix_col_width:
            for col, maxw in c2maxw.items():
                c2maxw[col] = max(maxw, len(header[col]))
                if wrap:
                    c2maxw[col] = min(c2maxw[col], max_col_width)
    else:
        current_item = 0
        row = items[current_item]
    while row:
        is_extra = False
        values = []
        extra_line = [""]*len(row)
        for col, val in enumerate(row):
            cwidth = c2maxw[col]
            wrap_width = cwidth
            val = str(val)
            try:
                newline_i = val.index("\n")
            except ValueError:
                pass
            else:
                wrap_width = min(newline_i+1, wrap_width)
                val = val.replace("\n", " ", 1)
            if wrap and len(val) > wrap_width:
                if wrap_style == "cut":
                    val = val[:wrap_width-1]+"+"
                elif wrap_style == "wrap":
                    extra_line[col] = val[wrap_width:]
                    val = val[:wrap_width]
            val = val.ljust(cwidth)
            values.append(val)
        print(' │ '.join(values))
        if not set(extra_line) - set(['']):
            if header and current_item == -1:
                print('═╪═'.join(['═'*c2maxw[col] for col in range(len(row)) ]))
            current_item += 1
            try:
                row = items[current_item]
            except IndexError:
                row = None
        else:
            row = extra_line
            is_extra = True

        if row_line and not is_extra and not (header and current_item == 0):
            if row:
                print('?╪═'.join(['-'*c2maxw[col] for col in range(len(row)) ]))
            else:
                print('!╪═'.join(['═'*c2maxw[col] for col in range(len(extra_line)) ]))



main()
