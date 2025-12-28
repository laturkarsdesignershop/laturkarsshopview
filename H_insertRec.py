

# now give me funtion to insert this data into database
# where the condition is like 

# if the id_order exist the updte complete record except id_order
# else insert the complete record



# {'id_order': 77570, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': '2025-12-09', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Pending', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0', 'cloth_bill': '0.0', 'stitching_bill': '0.0', 'cloth_balance': '0.0', 'stitching_advance': '0.0', 'stitching_balance': '0.0', 'serverup': 'no', 'measurestaff': '*'}





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



def emptyTable(conn, tableName):
    """
    Deletes all records from a given table.
    IO: conn MySQL connection, tableName str → None
    """
    try:
        cursor = conn.cursor()
        # Use backticks for table name to prevent SQL syntax errors
        query = f"DELETE FROM `{tableName}`"
        cursor.execute(query)
        conn.commit()
        print(f"✅ Table '{tableName}' emptied successfully.")
    except Error as e:
        print(f"❌ Error emptying table '{tableName}': {e}")





def upsertTailorOrder(conn, orderData):
    """
    Inserts or updates a record in tailor_order.
    If id_order exists, updates all fields except id_order.
    If id_order doesn't exist, inserts a new record.
    
    IO: conn MySQL connection, orderData dict → None
    """
    try:
        cursor = conn.cursor()
        
        # Check if id_order exists
        cursor.execute("SELECT id_order FROM tailor_order WHERE id_order = %s", (orderData['id_order'],))
        existing = cursor.fetchone()
        
        if existing:
            # Update all fields except id_order
            updateQuery = """
                UPDATE tailor_order
                SET id_customers=%s, order_date=%s, delivery_date=%s, delivery_time=%s, status=%s,
                    shirt_stipend=%s, pant_stipend=%s, shirt_cutting_stipend=%s, pant_cutting_stipend=%s,
                    shirt_stitching_price=%s, pant_stitching_price=%s, advance_payment=%s, total_payment=%s,
                    discount=%s, final_payment=%s, balance_payment=%s, payment_status=%s, cloth_payments=%s,
                    image=%s, metadata1=%s, metadata2=%s, measurestaff=%s,
                    product_balancecloth=%s, cloth_bill=%s, stitching_bill=%s, cloth_balance=%s,
                    stitching_advance=%s, stitching_balance=%s, serverup=%s
                WHERE id_order=%s
            """
            values = (
                orderData.get('id_customers'),
                orderData.get('order_date'),
                orderData.get('delivery_date'),
                orderData.get('delivery_time'),
                orderData.get('status'),
                orderData.get('shirt_stipend'),
                orderData.get('pant_stipend'),
                orderData.get('shirt_cutting_stipend'),
                orderData.get('pant_cutting_stipend'),
                orderData.get('shirt_stitching_price'),
                orderData.get('pant_stitching_price'),
                orderData.get('advance_payment'),
                orderData.get('total_payment'),
                orderData.get('discount'),
                orderData.get('final_payment'),
                orderData.get('balance_payment'),
                orderData.get('payment_status'),
                orderData.get('cloth_payments'),
                orderData.get('image'),
                orderData.get('metadata1'),
                orderData.get('metadata2'),
                orderData.get('measurestaff'),
                orderData.get('product_balancecloth'),
                orderData.get('cloth_bill'),
                orderData.get('stitching_bill'),
                orderData.get('cloth_balance'),
                orderData.get('stitching_advance'),
                orderData.get('stitching_balance'),
                orderData.get('serverup'),
                orderData.get('id_order')
            )
            cursor.execute(updateQuery, values)
            conn.commit()
            print(f"✅ Order {orderData['id_order']} updated successfully.")
        else:
            # Insert new record
            insertQuery = """
                INSERT INTO tailor_order (
                    id_order, id_customers, order_date, delivery_date, delivery_time, status,
                    shirt_stipend, pant_stipend, shirt_cutting_stipend, pant_cutting_stipend,
                    shirt_stitching_price, pant_stitching_price, advance_payment, total_payment,
                    discount, final_payment, balance_payment, payment_status, cloth_payments, image,
                    metadata1, metadata2, measurestaff, product_balancecloth, cloth_bill, stitching_bill,
                    cloth_balance, stitching_advance, stitching_balance, serverup
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                orderData.get('id_order'),
                orderData.get('id_customers'),
                orderData.get('order_date'),
                orderData.get('delivery_date'),
                orderData.get('delivery_time'),
                orderData.get('status'),
                orderData.get('shirt_stipend'),
                orderData.get('pant_stipend'),
                orderData.get('shirt_cutting_stipend'),
                orderData.get('pant_cutting_stipend'),
                orderData.get('shirt_stitching_price'),
                orderData.get('pant_stitching_price'),
                orderData.get('advance_payment'),
                orderData.get('total_payment'),
                orderData.get('discount'),
                orderData.get('final_payment'),
                orderData.get('balance_payment'),
                orderData.get('payment_status'),
                orderData.get('cloth_payments'),
                orderData.get('image'),
                orderData.get('metadata1'),
                orderData.get('metadata2'),
                orderData.get('measurestaff'),
                orderData.get('product_balancecloth'),
                orderData.get('cloth_bill'),
                orderData.get('stitching_bill'),
                orderData.get('cloth_balance'),
                orderData.get('stitching_advance'),
                orderData.get('stitching_balance'),
                orderData.get('serverup')
            )
            cursor.execute(insertQuery, values)
            conn.commit()
            print(f"✅ Order {orderData['id_order']} inserted successfully.")
    except Error as e:
        print(f"❌ Error in upsertTailorOrder: {e}")









if __name__ == "__main__":
    orderData = {
        'id_order': 77570, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': '2025-12-09',
        'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0,
        'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0,
        'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0,
        'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Pending', 'cloth_payments': 0.0,
        'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0',
        'cloth_bill': '0.0', 'stitching_bill': '0.0', 'cloth_balance': '0.0', 'stitching_advance': '0.0',
        'stitching_balance': '0.0', 'serverup': 'no', 'measurestaff': '*'
    }
    
    orderDataList = [
        {'id_order': 77570, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': '2025-12-09', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Pending', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0', 'cloth_bill': '0.0', 'stitching_bill': '0.0', 'cloth_balance': '0.0', 'stitching_advance': '0.0', 'stitching_balance': '0.0', 'serverup': 'no', 'measurestaff': '*'}, 
        {'id_order': 77569, 'id_customers': 35682, 'order_date': '2025-12-09', 'delivery_date': '2025-12-09', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 900.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Partly paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '420.0', 'stitching_bill': '580.0', 'cloth_balance': '0.0', 'stitching_advance': '480.0', 'stitching_balance': '100.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}, 
        {'id_order': 77568, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': '2025-11-22', 'delivery_time': None, 'status': 'Delivered', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 800.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Partly paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '520.0', 'stitching_bill': '480.0', 'cloth_balance': '0.0', 'stitching_advance': '280.0', 'stitching_balance': '200.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}, 
        {'id_order': 77567, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': '2025-11-22', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Not Paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '520.0', 'stitching_bill': '2260.0', 'cloth_balance': '520.0', 'stitching_advance': '0.0', 'stitching_balance': '2260.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}, 
        {'id_order': 77566, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': '2025-11-22', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Not Paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '0.0', 'stitching_bill': '1060.0', 'cloth_balance': '0.0', 'stitching_advance': '0.0', 'stitching_balance': '1060.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}, 
        {'id_order': 77565, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': None, 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Pending', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0', 'cloth_bill': '0.0', 'stitching_bill': '0.0', 'cloth_balance': '0.0', 'stitching_advance': '0.0', 'stitching_balance': '0.0', 'serverup': 'no', 'measurestaff': '*'}, 
        {'id_order': 77564, 'id_customers': 35681, 'order_date': '2025-12-09', 'delivery_date': None, 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Pending', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0', 'cloth_bill': '0.0', 'stitching_bill': '0.0', 'cloth_balance': '0.0', 'stitching_advance': '0.0', 'stitching_balance': '0.0', 'serverup': 'no', 'measurestaff': '*'}, 
        {'id_order': 77563, 'id_customers': 35681, 'order_date': '2025-12-08', 'delivery_date': '2025-11-22', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 0.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Not Paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '520.0', 'stitching_bill': '480.0', 'cloth_balance': '520.0', 'stitching_advance': '0.0', 'stitching_balance': '480.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}, 
        {'id_order': 77562, 'id_customers': 35681, 'order_date': '2025-12-07 21:14:23', 'delivery_date': '2025-11-22', 'delivery_time': None, 'status': 'New Order', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 500.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Partly paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '520.0', 'stitching_bill': '6630.0', 'cloth_balance': '20.0', 'stitching_advance': '0', 'stitching_balance': '6630.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}, 
        {'id_order': 77561, 'id_customers': 35681, 'order_date': '2025-12-07', 'delivery_date': '2025-11-11', 'delivery_time': None, 'status': 'Active', 'shirt_stipend': 0.0, 'pant_stipend': 0.0, 'shirt_cutting_stipend': 0.0, 'pant_cutting_stipend': 0.0, 'shirt_stitching_price': 0.0, 'pant_stitching_price': 0.0, 'advance_payment': 480.0, 'total_payment': 0.0, 'discount': 0.0, 'final_payment': 0.0, 'balance_payment': 0.0, 'payment_status': 'Partly paid', 'cloth_payments': 0.0, 'image': None, 'metadata1': 'testsales', 'metadata2': 'billingtest', 'product_balancecloth': '0.0', 'cloth_bill': '1000.0', 'stitching_bill': '480.0', 'cloth_balance': '520.0', 'stitching_advance': '0', 'stitching_balance': '480.0', 'serverup': 'no', 'measurestaff': 'measureStaff'}]


    conn = createConnection()
    if conn:
        # emptyTable(conn, "tailor_order")
        # emptyTable(conn, "tailor_products")
        # emptyTable(conn, "tailor_customers")
        # emptyTable(conn, "tailor_staff")
        
        
        # for orderData in orderDataList:
        #     upsertTailorOrder(conn, orderData)

    conn.close()


