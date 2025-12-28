from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

import requests, re, json
from functools import wraps
import base64, os, psutil, time, calendar
from datetime import date, datetime, timedelta
import socket, platform, httpagentparser, random, string

import io
from io import BytesIO
from calendar import monthrange

from PIL import Image, ImageDraw, ImageFont


import mysql.connector
from mysql.connector import Error




app = Flask(__name__)
app.secret_key = "myStrongSecretKey456"

defaultConfig = {    
    "Hosting_host" : "auth-db788.hstgr.io",
    "Hosting_database" : "u777474409_ltmobileview",
    "Hosting_user" : "u777474409_laturkarsmv",
    "Hosting_password" : "LaturkarsMV@1234"
    }

def createConnection():
    """
    Creates and returns MySQL DB connection
    IO: None → MySQL connection object
    """
    try:
        conn = mysql.connector.connect(
            host=defaultConfig["Hosting_host"],
            database=defaultConfig["Hosting_database"],
            user=defaultConfig["Hosting_user"],
            password=defaultConfig["Hosting_password"]
        )
        if conn.is_connected():
            print("Connection successful")
            return conn
    except Error as e:
        print(f"Connection error: {e}")
        return None




def convertDateFilter(inputDate):
    """
    Jinja filter to convert date YYYY-MM-DD to DD-MM-YYYY.
    IO: Takes string inputDate, returns converted string.
    Working: Splits date, rearranges and returns formatted value.
    """
    try:
        parts = inputDate.split("-")
        if len(parts) != 3:
            raise ValueError("Invalid date format")
        year, month, day = parts
        return f"{day}-{month}-{year}"
    except Exception as err:
        print(f"Error: {err}")
        return inputDate

app.jinja_env.filters["convertDate"] = convertDateFilter
    

@app.route("/")
def homePage():
    """
    Returns the mobile view welcome message for the root route.
    """
    try:
        # return "hello laturkars render mobil view"
        return render_template("dashboard.html")

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/aboutus")
def aboutUsPage():
    try:
        return "this is laturkars about us page"
    except Exception as error:
        return jsonify({"error": str(error)}), 500


















# ===========================================================================================
# Section: Order Routes 
# ===========================================================================================





def executeQuery(conn, query, params=None, fetchAll=False, fetchOne=False):
    """
    Execute SQL using MySQL connector.
    Supports select & update queries with automatic commit handling.
    """
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params or {})
        if fetchAll:
            return cursor.fetchall()
        if fetchOne:
            return cursor.fetchone()

        conn.commit()
        return True

    except Error as err:
        print(f"❌ SQL Error: {err}")
        return None


def getStaffNameById(conn, staffId):
    """
    Get staff fullname by staff ID.
    io:
        input: DB connection + staffId (int)
        output: fullname (str) or None if not found
    """
    try:
        if staffId is None:
            return "-"
        sql = """
            SELECT fullname 
            FROM tailor_staff
            WHERE id_staff = %(sid)s
            AND status != 'Deleted'
            LIMIT 1
        """
        result = executeQuery(conn,sql,{"sid": staffId},fetchOne=True)
        if result and result.get("fullname"):
            return result["fullname"]
        return "-"

    except Exception as err:
        print(f"❌ Failed to fetch staff name: {err}")
        return "-"



@app.route("/orders", methods=["GET", "POST"])
def listOrders():
    try:
        conn = createConnection()
        if not conn:
            flash("DB connection failed", "error")
            return redirect(url_for("dashboard"))

        keyword = request.args.get("keyword", "")
        page = int(request.args.get("page", 1))
        perPage = int(request.args.get("per_page", 10))
        todayDeliveries = []

        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()

            if keyword == "todaydeliveries":
                sqlToday = """
                    SELECT o.*, COALESCE(c.fullname, 'Unknown') AS customer_name,
                        COALESCE(c.phone, '') AS customer_phone,
                        COALESCE(c.mobile, '') AS customer_mobile
                    FROM tailor_order o
                    LEFT JOIN tailor_customers c 
                        ON o.id_customers = c.id_customers
                    WHERE o.delivery_date = %(todayDate)s
                    AND o.status != 'Deleted'
                    ORDER BY o.id_order DESC
                """
                todayDeliveries = executeQuery(
                    conn, sqlToday, {"todayDate": str(datetime.today().date())}, fetchAll=True)

            elif keyword == "todayorders":
                sqlTodayOrd = """
                    SELECT o.*, COALESCE(c.fullname, 'Unknown') AS customer_name,
                        COALESCE(c.phone, '') AS customer_phone,
                        COALESCE(c.mobile, '') AS customer_mobile
                    FROM tailor_order o
                    LEFT JOIN tailor_customers c 
                        ON o.id_customers = c.id_customers
                    WHERE o.order_date LIKE %(today)s
                    AND o.status != 'Deleted'
                    ORDER BY o.id_order DESC
                """
                todayDeliveries = executeQuery(
                    conn, sqlTodayOrd, {"today": f"{datetime.today().date()}%"}, fetchAll=True)

            page = 1

        if not todayDeliveries:
            kw = f"%{keyword}%"
            offset = (page - 1) * perPage

            sqlCount = """
                SELECT COUNT(*) as total
                FROM tailor_order
                WHERE id_order LIKE %(kw)s
                AND status != 'Deleted'
            """
            totalFiltered = executeQuery(conn, sqlCount, {"kw": kw}, fetchOne=True)["total"]

            sqlPaged = """
                SELECT o.*, COALESCE(c.fullname, 'Unknown') AS customer_name,
                    COALESCE(c.phone, '') AS customer_phone,
                    COALESCE(c.mobile, '') AS customer_mobile
                FROM tailor_order o
                LEFT JOIN tailor_customers c 
                    ON o.id_customers = c.id_customers
                WHERE o.id_order LIKE %(kw)s
                AND o.status != 'Deleted'
                ORDER BY o.id_order DESC
                LIMIT %(limit)s OFFSET %(offset)s
            """

            orders = executeQuery(conn, sqlPaged,
                {"kw": kw, "limit": perPage, "offset": offset}, fetchAll=True)

        else:
            orders = todayDeliveries
            totalFiltered = len(todayDeliveries)

        ordersWithStatuses = []

        for ordRow in orders:
            orderDict = dict(ordRow)

            sqlProducts = """SELECT * FROM tailor_products WHERE id_order=%(oid)s"""
            products = executeQuery(conn, sqlProducts, {"oid": orderDict["id_order"]}, fetchAll=True)
            
            cBill = float(orderDict.get("cloth_bill", 0.0))
            sBill = float(orderDict.get("stitching_bill", 0.0))
            
            totalBill = cBill + sBill
            advPay = float(orderDict.get("advance_payment", 0.0))
            balAmt = round(float(totalBill - advPay), 2)

            # orderDict["productStatuses"] = [row["status"] for row in products]
            orderDict["balAmt"] = balAmt
            orderDict["products"] = [row for row in products]
            
            for p in orderDict["products"]:
                p["p_stitching_staff"] = getStaffNameById(conn, p["id_staff"])
                p["p_cutting_staff"] = getStaffNameById(conn, p["cutting_staff"])
                
                
                jobStatus = None
                if "cut" in p["status"]:
                    jobStatus = "Cutting"

                elif "sew" in p["status"]:
                    jobStatus = "Stitching"

                elif "waiting" in p["status"]:
                    jobStatus = "Ready"

                elif "delivered" in p["status"]:
                    jobStatus = p["status"].upper()

                elif "new" in p["status"]:
                    jobStatus = p["status"].upper()

                else:
                    jobStatus = p["status"].upper()
                    
              
                    
                p["jobstatus"] = jobStatus
                print(f"Job Status: {jobStatus} | {p["cutting_return_date"]} | {p['stitching_return_date']}")

            ordersWithStatuses.append(orderDict)

        conn.close()

        ordersWithStatuses.sort(key=lambda o: int(o["id_order"]), reverse=True)

        return render_template(
            "orders/orderlist.html",
            orders=ordersWithStatuses,
            content={
                "orderDatalen": totalFiltered,
                "orderlen": totalFiltered,
                "keyword": keyword,
                "mainadmin": "myadmin",
                "page": page,
                "totalPages": (totalFiltered + perPage - 1) // perPage,
                "perPage": len(orders),
                "test_keywords": ["todaydeliveries", "todayorders"]
            }
        )

    except Exception as e:
        print(e)
        flash(f"Error fetching orders: {e}", "error")
        return redirect(url_for("homePage"))























































if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

