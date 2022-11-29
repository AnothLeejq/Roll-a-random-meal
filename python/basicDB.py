# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 22:21:13 2022

@author: 49280
"""
import mysql.connector
import python.basicDB
from mysql.connector import (connection)
from mysql.connector import errorcode
from datetime import datetime
from datetime import timedelta
import random
def create_database(cursor,DB_NAME):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
        return ["error","Failed creating database: {}".format(err)]

def database_write_line(connection_info,meal_date,meat_type,cook_method,meal_time,dressing_type):
    db_name = connection_info[3]
    
    if int(meal_date) < 20220101 or int(meal_date) > 22000000:
        return ["error","The date is invalid"]
    if len(meat_type) > 20 or len(cook_method) > 20 or len(dressing_type) > 20:
        return ["error","The message is too long"]
    if len(meat_type) <= 0 :
        meat_type = "No meat"
    if len(dressing_type) <= 0 :
        meat_type = "No dressing"
    if len(cook_method) <= 0 :
        cook_method = "Simple heat or no cook"
    #mysql_query = "INSERT INTO {}.mealslog (meal_date,meat_type,dressing_type,cook_method,meal_time) VALUES ({},%s,%s,%s,%s)".format(db_name,meal_date)
    mysql_query = "INSERT INTO {}.mealslog (meal_date,meat_type,dressing_type,cook_method,meal_time) VALUES ({},'{}','{}','{}','{}')".format(db_name,meal_date,meat_type,dressing_type,cook_method,meal_time)
    
    try:
        cnx = connection.MySQLConnection(user=connection_info[0], password=connection_info[1],
                                         host=connection_info[2],
                                         database=connection_info[3],auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        return ["error","value  did not get bacause: {}".format("Something is wrong with your user name or password")]
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        return ["error","value  did not get bacause: {}".format("Database does not exist")]
      else:
        print(err)
        return ["error","value  did not get bacause: {}".format(err)]
    else:
        try:
            cursor.execute(mysql_query)
            cnx.commit()
            cursor.close()
            cnx.close()
            return ["success","new log inserted: You {} {} and {} for your {}".format(cook_method,meat_type,dressing_type,meal_time)]
        except mysql.connector.Error as err:
            cursor.close()
            cnx.close()
            return ["error","new log did not created bacause: {}".format(err)]

def database_select_by_keys(connection_info,keyword,range,time="default"):
    currentDateAndTime = datetime.now()
    now_date = str(currentDateAndTime.strftime("%Y%m%d"))
    startDateAndTime = currentDateAndTime + timedelta(days = -range)
    start_date = str(startDateAndTime.strftime("%Y%m%d"))
    if time == "default":
        mysql_query = (
            "SELECT t1.{} FROM (SELECT {},meal_id "
            "FROM mealslog WHERE meal_date BETWEEN {} AND {}) AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(meal_id) FROM mealslog)-(SELECT MIN(meal_id) FROM mealslog))+(SELECT MIN(meal_id) FROM mealslog)) AS meal_id) AS t2 "
            "WHERE t1.meal_id >= t2.meal_id "
            "ORDER BY t1.meal_id LIMIT 1;").format(keyword,keyword,start_date,now_date)
    else:
        mysql_query = (
            "SELECT t1.{} FROM (SELECT {},meal_id "
            "FROM mealslog WHERE (meal_date BETWEEN {} AND {}) AND meal_time = '{}') AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(meal_id) FROM mealslog WHERE meal_time = '{}')-(SELECT MIN(meal_id) FROM mealslog WHERE meal_time = '{}'))+(SELECT MIN(meal_id) FROM mealslog WHERE meal_time = '{}')) AS meal_id) AS t2 "
            "WHERE t1.meal_id >= t2.meal_id "
            "ORDER BY t1.meal_id LIMIT 1;").format(keyword,keyword,start_date,now_date,time,time,time,time)
    try:
        cnx = connection.MySQLConnection(user=connection_info[0], password=connection_info[1],
                                         host=connection_info[2],
                                         database=connection_info[3],auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        return ["error","value  did not get bacause: {}".format("Something is wrong with your user name or password")]
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        return ["error","value  did not get bacause: {}".format("Database does not exist")]
      else:
        print(err)
        return ["error","value  did not get bacause: {}".format(err)]
    else:
        try:
            cursor.execute("USE {};".format(connection_info[3]))
            cursor.execute(mysql_query)
            rows = cursor.fetchall()
            result = ""
            for row in rows:
                result = row[0]
            cursor.close()
            cnx.close()
            return ["success","{}".format(result)]
        except mysql.connector.Error as err:
            cursor.close()
            cnx.close()
            return ["error","value of {} did not get bacause: {}".format(keyword,err)]

