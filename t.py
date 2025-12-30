import requests

def postSqlQuery(sqlQuery):
    """Send SQL query via POST and return response."""
    try:
        r = requests.post(
            "https://darkviolet-mosquito-473241.hostingersite.com/default.php",
            data={"sql": sqlQuery, "secretKey1": "thisis$!@$%Hostinger", "secretKey2": "Hostinger#123LatLong"},
            timeout=10
        )
        r.raise_for_status()
        return r.json() if r.headers.get("Content-Type") == "application/json" else {"responseText": r.text}
    except requests.RequestException as e:
        print("Error:", e)
        return None

# Example usage
print(postSqlQuery("SELECT fullname FROM tailor_staff"))
