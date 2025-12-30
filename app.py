import inspect
import traceback
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "myStrongSecretKey456"

# =======================
# SQL POST Helper
# =======================
def postSqlQuery(sqlQuery):
    """Send SQL query via POST and return response as dict."""
    try:
        print(f"🔑 Executing SQL: {sqlQuery}")
        r = requests.post(
            "https://darkviolet-mosquito-473241.hostingersite.com/default.php",
            data={
                "sql": sqlQuery,
                "secretKey1": "thisis$!@$%Hostinger",
                "secretKey2": "Hostinger#123LatLong"
            },
            timeout=10
        )
        r.raise_for_status()
        return r.json() if r.headers.get("Content-Type") == "application/json" else {"responseText": r.text}
    except requests.RequestException as e:
        print("❌ Error executing SQL:", e)
        print("Line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
        return None

def executeQuery(sql, fetchAll=False, fetchOne=False):
    """Execute SQL using postSqlQuery."""
    try:
        result = postSqlQuery(sql)
        if not result or not result.get("success"):
            return None
        data = result.get("data", [])
        if fetchOne:
            return data[0] if data else None
        if fetchAll:
            return data
        return True
    except Exception as e:
        print(f"❌ executeQuery Error: {e}")
        print("Line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
        return None

# =======================
# Utility Functions
# =======================
def convertDateFilter(inputDate):
    """Convert date from YYYY-MM-DD to DD-MM-YYYY."""
    try:
        if "-" not in inputDate:
            return inputDate
        parts = inputDate.split("-")
        if len(parts) != 3:
            raise ValueError("Invalid date format")
        year, month, day = parts
        return f"{day}-{month}-{year}"
    except Exception as err:
        print(f"Error Fun(convertDateFilter): {err}")
        print("Line:", traceback.extract_tb(err.__traceback__)[-1].lineno)
        return inputDate

app.jinja_env.filters["convertDate"] = convertDateFilter

# =======================
# Routes
# =======================
@app.route("/")
def homePage():
    """Render dashboard page."""
    try:
        return render_template("dashboard.html")
    except Exception as error:
        print("Line:", traceback.extract_tb(error.__traceback__)[-1].lineno)
        return jsonify({"error": str(error)}), 500

@app.route("/orders", methods=["GET", "POST"])
def listOrders():
    """List orders with optional filters."""
    try:
        keyword = request.args.get("keyword", "")
        page = int(request.args.get("page", 1))
        perPage = int(request.args.get("per_page", 10))
        todayDeliveries = []

        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()
            if keyword == "todaydeliveries":
                sqlToday = f"""
                    SELECT o.*, COALESCE(c.fullname, 'Unknown') AS customer_name,
                           COALESCE(c.phone, '') AS customer_phone,
                           COALESCE(c.mobile, '') AS customer_mobile
                    FROM tailor_order o
                    LEFT JOIN tailor_customers c ON o.id_customers = c.id_customers
                    WHERE o.delivery_date = '{datetime.today().date()}'
                    AND o.status != 'Deleted'
                    ORDER BY o.id_order DESC
                """
                todayDeliveries = executeQuery(sqlToday, fetchAll=True)
            elif keyword == "todayorders":
                sqlTodayOrd = f"""
                    SELECT o.*, COALESCE(c.fullname, 'Unknown') AS customer_name,
                           COALESCE(c.phone, '') AS customer_phone,
                           COALESCE(c.mobile, '') AS customer_mobile
                    FROM tailor_order o
                    LEFT JOIN tailor_customers c ON o.id_customers = c.id_customers
                    WHERE o.order_date LIKE '{datetime.today().date()}%'
                    AND o.status != 'Deleted'
                    ORDER BY o.id_order DESC
                """
                todayDeliveries = executeQuery(sqlTodayOrd, fetchAll=True)
            page = 1

        # Fetch orders for GET or POST keyword
        if not todayDeliveries:
            kw = f"%{keyword}%"
            offset = (page - 1) * perPage

            sqlCount = f"""
                SELECT COUNT(*) as total
                FROM tailor_order
                WHERE id_order LIKE '{kw}'
                AND status != 'Deleted'
            """
            # totalFiltered = executeQuery(sqlCount, fetchOne=True)["total"]
            totalFiltered = int(executeQuery(sqlCount, fetchOne=True)["total"])


            sqlPaged = f"""
                SELECT o.*, COALESCE(c.fullname, 'Unknown') AS customer_name,
                       COALESCE(c.phone, '') AS customer_phone,
                       COALESCE(c.mobile, '') AS customer_mobile
                FROM tailor_order o
                LEFT JOIN tailor_customers c ON o.id_customers = c.id_customers
                WHERE o.id_order LIKE '{kw}'
                AND o.status != 'Deleted'
                ORDER BY o.id_order DESC
                LIMIT {perPage} OFFSET {offset}
            """
            orders = executeQuery(sqlPaged, fetchAll=True)
        else:
            orders = todayDeliveries
            totalFiltered = len(todayDeliveries)

        # -------------------------
        # Batch fetch products & staff
        # -------------------------
        orderIds = [o["id_order"] for o in orders]
        productsSql = f"SELECT * FROM tailor_products WHERE id_order IN ({','.join(map(str, orderIds))})"
        allProducts = executeQuery(productsSql, fetchAll=True) or []

        orderProductMap = {oid: [] for oid in orderIds}
        staffIds = set()
        for p in allProducts:
            orderProductMap[p["id_order"]].append(p)
            if p.get("id_staff"):
                staffIds.add(p["id_staff"])
            if p.get("cutting_staff"):
                staffIds.add(p["cutting_staff"])

        staffMap = {}
        if staffIds:
            staffSql = f"SELECT id_staff, fullname FROM tailor_staff WHERE id_staff IN ({','.join(map(str, staffIds))}) AND status != 'Deleted'"
            staffData = executeQuery(staffSql, fetchAll=True) or []
            staffMap = {s['id_staff']: s['fullname'] for s in staffData}

        ordersWithStatuses = []
        for ordRow in orders:
            orderDict = dict(ordRow)
            orderDict["products"] = orderProductMap.get(orderDict["id_order"], [])
            cBill = float(orderDict.get("cloth_bill", 0.0))
            sBill = float(orderDict.get("stitching_bill", 0.0))
            advPay = float(orderDict.get("advance_payment", 0.0))
            orderDict["balAmt"] = round(cBill + sBill - advPay, 2)

            for p in orderDict["products"]:
                p["p_stitching_staff"] = staffMap.get(p.get("id_staff"), "-")
                p["p_cutting_staff"] = staffMap.get(p.get("cutting_staff"), "-")

                status = p.get("status", "").lower()
                if "cut" in status:
                    jobStatus = "Cutting"
                elif "sew" in status:
                    jobStatus = "Stitching"
                elif "waiting" in status:
                    jobStatus = "Ready"
                elif "delivered" in status or "new" in status:
                    jobStatus = status.upper()
                else:
                    jobStatus = status.upper()
                p["jobstatus"] = jobStatus

            ordersWithStatuses.append(orderDict)

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
        print("❌ Error fetching orders:", e)
        tb = traceback.extract_tb(e.__traceback__)
        if tb:
            print("Error Line:", tb[-1].lineno)  # prints only the line number
        flash(f"Error fetching orders: {e}", "error")
        return redirect(url_for("homePage"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
