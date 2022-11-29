# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 22:10:17 2022

@author: 49280
"""
import mysql.connector
import python.basicDB
from mysql.connector import (connection)
from mysql.connector import errorcode
from mysql.connector.locales.eng import client_error
def onload_database(connection_info):
    DB_NAME = connection_info[3]
    try:
        cnx = connection.MySQLConnection(user=connection_info[0], password=connection_info[1],
                                         host=connection_info[2],
                                         database=connection_info[3],auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
    
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)

    else:
        try:
            cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                basicDB.create_database(cursor,DB_NAME)
                print("Database {} created successfully.".format(DB_NAME))
                cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

        try:
      
              TABLES = {}
              TABLES['mealslog'] = (
                    "CREATE TABLE `mealslog` ("
                    "  `meal_id` int(11) NOT NULL AUTO_INCREMENT,"
                    "  `meal_date` date NOT NULL,"
                    "  `meat_type` varchar(20),"
                    "  `cook_method` varchar(20) NOT NULL,"
                    "  `meal_time` enum('breakfast','lunch','dinner') NOT NULL,"
                    "  `dressing_type` varchar(20),"
                    "  PRIMARY KEY (`meal_id`)"
                    ") ENGINE=InnoDB")
    
        except mysql.connector.Error as err:
            print(err)
        else:
            for table_name in TABLES:
                table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()
        cnx.close()


