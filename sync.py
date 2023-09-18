import pymssql

conn = pymssql.connect(
    server='192.168.20.9',
    user='fm1234',
    password='x2y2',
    database='Formula',
    as_dict=True
)  

SQL_QUERY = f"""select FCSKID,FCCODE,FCNAME from COOR c order by c.FCCODE"""
cursor = conn.cursor()
cursor.execute(SQL_QUERY)

for r in cursor.fetchall():
     print(f"{r['FCSKID']}\t{r['FCCODE']}\t{r['FCNAME']}")

cursor.close()
conn.close()