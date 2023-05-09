# import pymysql
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
#
# endpoint = 'database-1.cv70rzejhsog.us-east-1.rds.amazonaws.com'
# username='admin'
# password='519android'
# database_name='MobileClassFinalProject'
#
#
# connection = pymysql.connect(host=endpoint, port=3306, user=username, passwd=password, db=database_name)
#
# def lambda_handler(event, context):
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM trip')
#
#     rows = cursor.fetchall()
#
#     for row in rows:
#         print(row)

