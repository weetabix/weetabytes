#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode

import sys
sys.path.insert(0, '.')

import tables



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(table.DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


#print(tables.TABLES)

#print('load')

try:
  cnx = mysql.connector.connect(user='uomi', password='B9cSPPc73AKUSuX6',
                              host='kibostor',
                              database='uomi')

except mysql.connector.Error as err:
  print(err)
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password,\nor you don't have permission to that db.")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    create_database()
  else:
    print("Some other error has occured")
    print(err)
else:
  cnx.close()

