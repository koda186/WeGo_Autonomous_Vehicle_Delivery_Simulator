import pymysql
import bcrypt


def registerUser(email, companyName, password):
    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    password = password.encode("utf-8")
    hashedPasswordBytes = bcrypt.hashpw(password, bcrypt.gensalt())
    hashedPassword = hashedPasswordBytes.decode("utf-8")
    query = ("""INSERT INTO fleet_managers(companyName, email, password) VALUES('%s', '%s', '%s');""")
    query = query % (companyName, email, hashedPassword)
    print(query)
    cursor.execute(query)
    conn.commit()
    print("Fleet Manager account created successfully")
    conn.close()

    return "Successfully registered user"


# email is the same as UserID
def loginUser(email, password):
    conn = pymysql.connect(host="localhost", user="team12", passwd="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("""SELECT email, password from fleet_managers where email='%s';""")
    query = query % (email)
    cursor.execute(query)
    rows = cursor.fetchall()
    password = password.encode("utf-8")
    print(password)
    fetchedEmail = rows[0][0]
    fetchedPassword = rows[0][1]
    print("Email: " + fetchedEmail)
    print("Password: " + fetchedPassword)
    fetchedPassword = fetchedPassword.encode("utf-8")
    print(rows)
    try:
        if (fetchedEmail == email) and (bcrypt.checkpw(password, fetchedPassword)):
            return 1
        else:
            return 0
    except Exception as error:
        return error
    conn.close()
