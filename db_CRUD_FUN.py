import mysql.connector
from mysql.connector import Error
import uuid

import config

def createConnection():
    """
    Creates and returns a MySQL database connection object.
    Output: MySQL connection object
    """
    try:
        conn = mysql.connector.connect(
            host="auth-db788.hstgr.io",
            database="u777474409_softwardata",
            user="u777474409_softUSER456",
            password="SoftUser@1234"
        )
        if conn.is_connected():
            print("✅ MySQL connection established successfully.")
            return conn
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None


def createTable(conn):
    """
    Creates a table 'testdata' with id, name, and number columns if not exists.
    Input: conn (MySQL connection object)
    Output: None
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS testdata (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100),
                number VARCHAR(15)
            )
        """)
        conn.commit()
        print("✅ Table 'testdata' created successfully.")
    except Error as e:
        print(f"❌ Error while creating table: {e}")


def insertRecord(conn, recordId, name, number):
    """
    Inserts one record into 'testdata' table.
    Input: recordId (UUID string), name (str), number (str)
    Output: None
    """
    try:
        cursor = conn.cursor()
        query = "INSERT INTO testdata (id, name, number) VALUES (%s, %s, %s)"
        cursor.execute(query, (recordId, name, number))
        conn.commit()
        print(f"✅ Record inserted successfully: {name}")
    except Error as e:
        print(f"❌ Error while inserting record: {e}")


def getAllRecords(conn):
    """
    Fetches all records from 'testdata'.
    Input: conn (MySQL connection object)
    Output: List of all records
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testdata")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"❌ Error while fetching records: {e}")
        return []


def getRecordById(conn, recordId):
    """
    Fetches one record by ID.
    Input: recordId (UUID string)
    Output: Single record tuple
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testdata WHERE id = %s", (recordId,))
        row = cursor.fetchone()
        return row
    except Error as e:
        print(f"❌ Error while fetching record by ID: {e}")
        return None


def updateRecordById(conn, recordId, newName, newNumber):
    """
    Updates name and number of a record by ID.
    Input: recordId (UUID string), newName (str), newNumber (str)
    Output: None
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE testdata 
            SET name = %s, number = %s 
            WHERE id = %s
        """, (newName, newNumber, recordId))
        conn.commit()
        print(f"✅ Record with ID {recordId} updated successfully.")
    except Error as e:
        print(f"❌ Error while updating record: {e}")


# ====================== TEST FUNCTION CALLS ======================

if __name__ == "__main__":


    conn = createConnection()
    print(f"\n🔑 MySQL connection object: {conn}")
    if conn:
        # createTable(conn)

        # # Insert 2 records
        # id1 = str(uuid.uuid4())
        # id2 = str(uuid.uuid4())
        # insertRecord(conn, id1, "Atharva Pawar", "9876543210")
        # insertRecord(conn, id2, "John Doe", "9123456789")

        # Fetch all
        print("\n📋 All Records:")
        for r in getAllRecords(conn):
            print(r)

        # # Fetch by ID
        # print(f"\n🔍 Record by ID ({id1}):")
        # print(getRecordById(conn, id1))

        # # Update record by ID
        # updateRecordById(conn, id2, "Jane Doe", "9000000000")

        # Fetch all again to confirm update
        print("\n📋 Updated Records:")
        for r in getAllRecords(conn):
            print(r)

        conn.close()
        print("\n🔒 MySQL connection closed.")
    else:
        print("\n❌ MySQL connection failed.")