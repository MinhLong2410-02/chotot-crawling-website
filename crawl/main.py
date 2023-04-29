from fastapi import FastAPI
from utils import *
import mysql.connector as connector
from uvicorn import run
host = "host.docker.internal"
port = '6603'
database = 'PHONES'

app = FastAPI()

@app.post("/crawl/{shop_id}")
def crawl_data(shop_id: str):
    cnx = connector.connect(user='root', password='psw123', port=port, host=host, database=database)
    try:
        create_table(cnx)
    except:
        print("Table already exists")
    query = "SELECT shop_id FROM shops WHERE shop_id = %s"
    cursor = cnx.cursor()
    data = execute(cursor, query, (shop_id,))
    if len(data) == 0:
        insert_shop_to_db(cnx, shop_id)
        data = crawl(shop_id)
        insert_to_db(cnx, data)
        
        cnx.close()
        return {"status": True, "message": f"{shop_id} đã được cào thành công"}
        
    
    query = "SELECT * FROM phones WHERE shop_id = %s"
    cursor = cnx.cursor()
    
    data = execute(cursor, query, (shop_id,))
    if len(data) > 0:
        return {"status": False, "message": f"{shop_id} đã được cào trước đó"}
    
    data = crawl(shop_id)
    insert_to_db(cnx, data)
    
    cnx.close()
    return {"status": True, "message": f"{shop_id} đã được cào thành công"}



run(app, host="0.0.0.0", port=9001)