import pymysql.cursors


def insertOrderIntoDB(serviceType, destinationAddress, username):
    db = pymysql.connect(host="localhost", user="team12", passwd="pandapanda", db="team12_wego")
    cursor = db.cursor()

    sql = ("""INSERT INTO ServiceRecord(serviceType, destinationAddress, username, dispatchVehicle) VALUES (%s, %s, %s, NULL)""")
    insert_tuple = (serviceType, destinationAddress, username)

    cursor.execute(sql, insert_tuple)
    db.commit()

    return "Successfully added order"

    cursor.close()
    db.close()
