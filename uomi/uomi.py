#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta


def main():
    """Main is here so I can hide long ugly lists of SQL variables at the bottom."""
    try:
        cnx = mysql.connector.connect(user='uomi', password='B9cSPPc73AKUSuX6', host='kibostor')
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print(err)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password,\nor you don't have permission to that db.")
        else:
            print("Some other error has occured")
            print(err)
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Call Make DB")
            create_database(cursor)
            cnx.database = DB_NAME
            print("Call Make Tables")
            create_tables(cursor)
        else:
            print(err)
            exit(1)

    add_debt(cursor)
    print_debt(cursor)
    add_credit(cursor)
    print_credit(cursor)
    cursor.close()
    cnx.close()


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
    person = input('Enter your name: ')
    while True:
        type = input('(C)ash (B)arter (O)ther')
        if type in ['C','B', 'O']:
            break
    debt = "INSERT INTO debt (date, name, type, value, barter, other, pay_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    amount = 250
    payback = datetime.now().date() + timedelta(seconds=160000 + (((amount ** 0.5) * 1.5) * 90000))
    today = datetime.now().date()
    debt_data = (today, person, "barter", "", "Canoue", "", payback)
    in_cursor.execute(debt, debt_data)
    print(in_cursor.lastrowid)


def print_debt(in_cursor):
    """Print all the debts I owe"""
    query = "SELECT `debt_no`, `date`, `name`, `type`, `value`, `barter`, `other`, `pay_date` FROM `debt` WHERE 1"
    in_cursor.execute(query)
    total = 0
    for rec in in_cursor:
        total += int(rec[4])
#       derp = [str(rec[i]) for i in [0,1,2,3,4,5,6,7] if rec[3] == "cash"]
        derp = [str(rec[i]) for i in [0, 1, 2, 3, 4, 5, 6, 7]]
#       print(derp)
        print(' '.join(derp))
    print("Cash ",total)


def add_credit(in_cursor):
    """Insert a credit I am owed into the database.
    Repay time is calculated as 2 days plus a little over a day for
    every $13 or so on a sliding scale."""
    person = input('Enter name: ')
    while True:
        type = input('(C)ash (B)arter (O)ther')
        if type in ['C','B', 'O']:
            break
    credit = "INSERT INTO credit (date, name, type, value, barter, other, pay_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    amount = 250
    payback = datetime.now().date() + timedelta(seconds=160000 + (((amount ** 0.5) * 1.5) * 90000))
    today = datetime.now().date()
    credit_data = (today, person, "cash", "11", "", "", payback)
    in_cursor.execute(credit, credit_data)
    print(in_cursor.lastrowid)


def print_credit(in_cursor):
    """Print all the credit owed me."""
    query = "SELECT `credit_no`, `date`, `name`, `type`, `value`, `barter`, `other`, `pay_date` FROM `credit` WHERE 1"
    in_cursor.execute(query)
    total = 0
    for rec in in_cursor:
        total += int(rec[4])
#       derp = [str(rec[i]) for i in [0,1,2,3,4,5,6,7] if rec[3] == "cash"]
        derp = [str(rec[i]) for i in [0, 1, 2, 3, 4, 5, 6, 7]]
#       print(derp)
        print(' '.join(derp))
    print("Cash ",total)


DB_NAME = 'uomi'
TABLES = {}
TABLES['debt'] = (
    "CREATE TABLE `debt` ("
    "  `debt_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `name` varchar(30) NOT NULL,"
    "  `type` enum('cash','barter','other') NOT NULL,"
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
    "  `type` enum('cash','barter','other') NOT NULL,"
    "  `value` int(11) NULL,"
    "  `barter` varchar(128) NULL,"
    "  `other` varchar(128) NULL,"
    "  `pay_date` date NOT NULL,"
    "  PRIMARY KEY (`credit_no`)"
    ") ENGINE=MyISAM")

main()
