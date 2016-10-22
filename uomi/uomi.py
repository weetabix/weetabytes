#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
import os
import argparse

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
    print('\nUoMi\n\n')
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
            print_debt(cursor)
            cnx.commit()
#            cursor.close()
#            cnx.close()
        elif args.type == "+C":
            delete_credit(cursor, cnx)
            print_credit(cursor)
            cnx.commit()
#            cursor.close()
#            cnx.close()
    else:
        print("\n")
        print('{:═^80}'.format(" Debts "))
        print_debt(cursor)
        print("\n")
        print('{:═^80}'.format(" Credits "))
        print_credit(cursor)


"""        debcred = input('(d)ebt, (c)redit\n')
        if debcred in ['d', 'c']:
            if debcred == 'd':
                add_debt(cursor)
                print_debt(cursor)
                cursor.close()
                cnx.close()
            elif debcred == 'c':
                add_credit(cursor)
                print_credit(cursor)
                cursor.close()
                cnx.close()
        else:
            cursor.close()
            cnx.close()
"""


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
    for rec in in_cursor:
        total += int(rec[4])
        r = [str(rec[i]) for i in range(0, 8)]  # Reordering the record too.
        print('{} {} {} {:12} ${:5} {:16} {:16} {}'.format(r[0], r[1], r[3], r[2], r[4], r[5], r[6], r[7]))
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
    for rec in in_cursor:
        total += int(rec[4])
        r = [str(rec[i]) for i in range(0, 8)]  # Reordering the record too.
        print('{} {} {} {:12} ${:5} {:16} {:16} {}'.format(r[0], r[1], r[3], r[2], r[4], r[5], r[6], r[7]))
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

main()
