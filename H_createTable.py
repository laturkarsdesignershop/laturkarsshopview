import config
import mysql.connector
from mysql.connector import Error

def createConnection():
    """
    Creates and returns MySQL DB connection
    IO: None → MySQL connection object
    """
    try:
        conn = mysql.connector.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password
        )
        if conn.is_connected():
            print("Connection successful")
            return conn
    except Error as e:
        print(f"Connection error: {e}")
        return None


def createTailorOrderTable(conn):
    """
    Creates tailor_order table if not exists
    IO: conn MySQL connection → None
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tailor_order (
                id_order INTEGER PRIMARY KEY,
                id_customers INTEGER,
                order_date TEXT,
                delivery_date TEXT,
                delivery_time TEXT,
                status TEXT,
                shirt_stipend REAL,
                pant_stipend REAL,
                shirt_cutting_stipend REAL,
                pant_cutting_stipend REAL,
                shirt_stitching_price REAL,
                pant_stitching_price REAL,
                advance_payment REAL,
                total_payment REAL,
                discount REAL,
                final_payment REAL,
                balance_payment REAL,
                payment_status TEXT,
                cloth_payments REAL,
                image TEXT,
                metadata1 TEXT DEFAULT '*',
                metadata2 TEXT DEFAULT '*',
                measurestaff TEXT DEFAULT '*',
                product_balancecloth TEXT DEFAULT '0',
                cloth_bill TEXT DEFAULT '0.0',
                stitching_bill TEXT DEFAULT '0.0',
                cloth_balance TEXT DEFAULT '0.0',
                stitching_advance TEXT DEFAULT '0.0',
                stitching_balance TEXT DEFAULT '0.0',
                serverup TEXT DEFAULT 'no'
            )
        """)
        conn.commit()
        print("Table tailor_order created")
    except Error as e:
        print(f"Error creating tailor_order: {e}")


def createTailorProductsTable(conn):
    """
    Creates tailor_products table if not exists
    IO: conn MySQL connection → None
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tailor_products (
                id_product INTEGER PRIMARY KEY,
                id_order INTEGER,
                id_staff INTEGER,
                cutting_staff INTEGER,
                id_customers INTEGER,
                id_main_cat INTEGER,
                id_cat INTEGER,
                qty INTEGER,
                shirt_type TEXT,
                shirt_sub_type TEXT,
                pocket_type TEXT,
                collar_type TEXT,
                cuff_type TEXT,
                patti_type TEXT,
                cut_type TEXT,
                shirt_height TEXT,
                shirt_munda TEXT,
                shirt_chest TEXT,
                shirt_front_loose_1 TEXT,
                shirt_front_loose_2 TEXT,
                shirt_front_loose_3 TEXT,
                shirt_stomach_width TEXT,
                shirt_seat TEXT,
                shoulder_width TEXT,
                shoulder_down TEXT,
                astin_width TEXT,
                astin_loose_width TEXT,
                collor_width TEXT,
                cuff_width TEXT,
                shirt_description TEXT,
                pant_type TEXT,
                pant_press TEXT,
                pant_sub_type TEXT,
                pant_front_pocket_type TEXT,
                pant_back_pocket_type TEXT,
                pant_watch_pocket_type TEXT,
                pant_height TEXT,
                many TEXT,
                pant_waist_width TEXT,
                pant_seat_width TEXT,
                thigh_width TEXT,
                knee TEXT,
                pant_bottom TEXT,
                hl_waist TEXT,
                low_waist_text TEXT,
                pant_description TEXT,
                status TEXT,
                image TEXT,
                stipend REAL,
                stipend_status TEXT,
                cutting_stipend REAL,
                cutting_stipend_status TEXT,
                stitching_price REAL,
                cutting_allote_date TEXT,
                cutting_return_date TEXT,
                stitching_allote_date TEXT,
                stitching_return_date TEXT,
                metadata1 TEXT DEFAULT '*',
                metadata2 TEXT DEFAULT '*',
                clothunit TEXT DEFAULT '0.0',
                clothtype TEXT DEFAULT '*',
                clothcost TEXT DEFAULT '0.0',
                totalamount TEXT DEFAULT '0.0',
                product_balancecloth TEXT DEFAULT '0',
                urgentinfo TEXT DEFAULT '*',
                itemcost TEXT DEFAULT '0.0',
                gender TEXT DEFAULT 'male',
                serverup TEXT DEFAULT 'no',
                barcodeimg TEXT DEFAULT '*'
            )
        """)
        conn.commit()
        print("Table tailor_products created")
    except Error as e:
        print(f"Error creating tailor_products: {e}")




def createTailorCustomersTable(conn):
    """
    Creates tailor_customers table if not exists
    IO: conn MySQL connection → None
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tailor_customers (
                id_customers INTEGER PRIMARY KEY,
                address TEXT,
                phone TEXT,
                joindate TEXT,
                mobile TEXT,
                status TEXT,
                metadata1 TEXT DEFAULT '*',
                metadata2 TEXT DEFAULT '*',
                fullname TEXT,
                serverup TEXT DEFAULT 'no'
            )
        """)
        conn.commit()
        print("Table tailor_customers created")
    except Error as e:
        print(f"Error creating tailor_customers: {e}")


def createTailorStaffTable(conn):
    """
    Creates tailor_staff table if not exists
    IO: conn MySQL connection → None
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tailor_staff (
                id_staff INTEGER PRIMARY KEY,
                id_cat INTEGER NOT NULL,
                staff_type INTEGER,
                address TEXT,
                phone TEXT,
                mobile TEXT,
                dob TEXT,
                joindate TEXT,
                status TEXT,
                image TEXT,
                metadata1 TEXT DEFAULT '*',
                fullname TEXT,
                salary TEXT DEFAULT '0.0',
                backpocketamt TEXT DEFAULT '0.0',
                shirtcuttingamt TEXT DEFAULT '0.0',
                shirtstitchingamt TEXT DEFAULT '0.0',
                pantcuttingamt TEXT DEFAULT '0.0',
                pantstitchingamt TEXT DEFAULT '0.0',
                plus42shirtamt TEXT DEFAULT '0.0',
                plus42pantamt TEXT DEFAULT '0.0',
                cuffling TEXT DEFAULT '0.0',
                stylestipendjson TEXT DEFAULT '[]',
                serverup TEXT DEFAULT 'no'
            )
        """)
        conn.commit()
        print("✅ Table tailor_staff created successfully.")
    except Error as e:
        print(f"❌ Error creating tailor_staff: {e}")





if __name__ == "__main__":
    dbConn = createConnection()
    if dbConn:
        # createTailorOrderTable(dbConn)
        # createTailorProductsTable(dbConn)
        # createTailorCustomersTable(dbConn)

        # createTailorStaffTable(dbConn)

        dbConn.close()
        print("DB closed")
    else:
        print("DB connection failed")




