import pyodbc
import requests
import json

# Set your SQL Server connection parameter
server = '192.168.20.9'
database = 'Formula'
username = 'fm1234'
password = 'x2y2'

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
# Establish a connection
conn = pyodbc.connect(connection_string)

url = "http://localhost:8000/api"
payload = json.dumps({
    "usr": "Administrator",
    "pwd": "admin@vcs"
})
headers = {'Content-Type': 'application/json'}
session = requests.request(
    "POST", f"{url}/method/login", headers=headers, data=payload)
if session.status_code == 200:
    response = requests.request(
        "GET", f"{url}/method/frappe.auth.get_logged_user", cookies=session.cookies)
    print(response.json())

SQL_QUERY = f"""select FCSKID,FCCODE,FCNAME from COOR c order by c.FCCODE"""
cursor = conn.cursor()
cursor.execute(SQL_QUERY)

i = 1
for r in cursor.fetchall():
    FCSKID = str(f"{r[0]}").strip()
    FCCODE = str(f"{r[1]}").strip()
    FCNAME = str(f"{r[2]}").strip()

    print(f"FCSKID:{FCSKID} FCCODE:{FCCODE} FCNAME: {FCNAME}")
    payload = json.dumps({
      "fcskid": FCSKID,
      "code": FCCODE,
      "supplier_name": FCNAME
    })
    headers = {'Content-Type': 'application/json',}
    response = requests.request("POST", f"{url}/resource/Supplier Manangement", headers=headers, data=payload, cookies=session.cookies)

    print(f"{i}.Sync Status Code:{response.status_code}")
    i += 1

cursor.close()
conn.close()

response = requests.request("GET", f"{url}/method/logout", cookies=session.cookies)
