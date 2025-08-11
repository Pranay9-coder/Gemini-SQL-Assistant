import sqlite3

connection= sqlite3.connect("student.db")

#cursor
cursor=connection.cursor()

##create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
                     SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

##insert the data
cursor.execute('''Insert Into STUDENT values('Pranay','Gen AI','A',100)''')
cursor.execute('''Insert Into STUDENT values('Rohit','AI','A',90)''')
cursor.execute('''Insert Into STUDENT values('Yash','ML','B',95)''')
cursor.execute('''Insert Into STUDENT values('Nitin','Gen AI','A',91)''')
cursor.execute('''Insert Into STUDENT values('Manish','AI','B',90)''')

##Display

print("The inserted records are")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

##Commit your chnage
connection.commit()
connection.close()
