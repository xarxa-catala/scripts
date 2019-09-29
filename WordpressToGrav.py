import mysql.connector
import string
import random

conn = mysql.connector.connect(host="localhost",
                               database="database",
                               user="user",
                               password="passwd")

sql_select = "select user_login, user_email, display_name from wp_users"
cursor = conn.cursor()
cursor.execute(sql_select)
rows = cursor.fetchall()

for row in rows:
    user = row[0]
    email = row[1]
    name = row[2]
    f = open(user+".yaml", "w")
    l1 = "state: enabled\n"
    l2 = "email: " + email + "\n"
    l3 = "fullname: " + name  + "\n"
    l4 = "access:\n"
    l5 = "  site:\n"
    l6 = "    login: true\n"
    l7 = "hashed_password: " + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)) + "\n"
    f.writelines([l1, l2, l3, l4, l5, l6, l7])
    f.close()
