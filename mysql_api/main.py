import json
import requests
import mysql.connector as connector
from fastapi import FastAPI
from typing import Optional
from utils import *
from uvicorn import run
host = "host.docker.internal"
port = '6603'

database = 'PHONES'
def create_table(cnx):
    query = '''
        USE PHONES;
        CREATE TABLE phones (
            ad_id VARCHAR(255) NOT NULL,
            shop_id VARCHAR(255) NOT NULL,
            region_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            price INT NOT NULL,
            price_string VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            subject_content VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            can_deposit TINYINT NOT NULL,
            body TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            image_url VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            PRIMARY KEY (ad_id)
        );


        CREATE TABLE cud(
            number_of_created INT NOT NULL,
            number_of_updated INT NOT NULL,
            number_of_deleted INT NOT NULL
        );
        insert into cud values (0, 0, 0);

        CREATE TABLE shops(
            shop_id VARCHAR(255) NOT NULL,
            PRIMARY KEY (shop_id)
        );
        insert into shops values ('143820887');
        insert into shops values ('139931303');
        insert into shops values ('128013841');
        insert into shops values ('142445059');
        insert into shops values ('132053691');
        insert into shops values ('138953767');
        insert into shops values ('144157887');
        insert into shops values ('144985040');
        '''
    cursor = cnx.cursor()
    execute(cursor, query, multi=True)
    cnx.commit()


app = FastAPI()

@app.get("/shops")
def shops():
    cnx = connector.connect(user='root', password='psw123', port=port, host=host, database=database)
    cursor = cnx.cursor()
    try:
        create_table(cnx)
    except:
        print("Table already exists")
    
    query = "SELECT shop_id FROM shops"
    data = execute(cursor, query)
    cnx.close()
    return {"Một số id của các shop bán điện thoại": data}

@app.get("/phone")
def phone(subject_content: Optional[str] = None, region_name: Optional[str] = None, price: Optional[int] = None):
    cnx = connector.connect(user='root', password='psw123', port='6603', host=host, database=database)
    cursor = cnx.cursor()
    try:
        create_table(cnx)
    except:
        print("Table already exists")
    values = []
    if subject_content:
        query = "SELECT * FROM phones WHERE subject_content LIKE %s"
        values.append(f"%{subject_content}%")
        if region_name:
            query += " AND region_name = %s"
            values.append(region_name)
        if price:
            query += " AND price = %s"
            values.append(price)
    elif region_name:
        query = "SELECT * FROM phones WHERE region_name = %s"
        if price:
            query += " AND price = %s"
            values.append(price)
    elif price:
        query = "SELECT * FROM phones WHERE price = %s"
    
    if len(values) == 0:
        query = "SELECT * FROM phones"
        data = execute(cursor, query)
        return data
    values = tuple(values)
    data = execute(cursor, query, values)
    cnx.close()
    
    return data

@app.get("/phone/{shop_id}")
def phone_id(shop_id: str, ad_id: Optional[str] = None):
    cnx = connector.connect(user='root', password='psw123', port='6603', host=host, database=database)
    try:
        create_table(cnx)
    except:
        print("Table already exists")
    cursor = cnx.cursor()
    try:
        if ad_id:
            query = "SELECT * FROM phones WHERE shop_id = %s AND ad_id = %s"
            values = (shop_id, ad_id)
            data = execute(cursor, query, values)
            return data
        query = "SELECT * FROM phones WHERE shop_id = %s"
        values = (shop_id,)
        data = execute(cursor, query, values)
    except:
        create_table()
    if ad_id:
        query = "SELECT * FROM phones WHERE shop_id = %s AND ad_id = %s"
        values = (shop_id, ad_id)
        data = execute(cursor, query, values)
        return data
    query = "SELECT * FROM phones WHERE shop_id = %s"
    values = (shop_id,)
    
    cnx.close()
    return data
@app.get("/price-range")
def price_range(min_price: int, max_price: int):
    cnx = connector.connect(user='root', password='psw123', port='6603', host=host, database=database)
    try:
        create_table(cnx)
    except:
        print("Table already exists")
    cursor = cnx.cursor()
    
    query = "SELECT * FROM phones WHERE price BETWEEN %s AND %s"
    values = (min_price, max_price)
    data = execute(cursor, query, values)
    cnx.close()
    return data
    
@app.get("/CUD")
def CUD():
    cnx = connector.connect(user='root', password='psw123', port='6603', host=host, database=database)
    try:
        create_table(cnx)
    except:
        print("Table already exists")
    cursor = cnx.cursor()
    query = "SELECT * FROM cud"
    data = execute(cursor, query)
    data = {'messages': "chỉ số create-update-delete gần đây nhất", 'data': data[-1]}
    cnx.close()
    
    return data
    
    
@app.get("/crawl/{shop_id}")
def crawl_data(shop_id: str):
    cnx = connector.connect(user='root', password='psw123', port='6603', host=host, database=database)
    cursor = cnx.cursor()
    res = requests.get(f"http://crawl:9001/crawl/{shop_id}").json()
    if res['status']:
        update_cud(cursor, 'number_of_created')
        cnx.commit()
    else:
        cud = {"status": False, "message": "Không crawl thành công"}
    cnx.close()
    return cud

@app.get("/delete")
def delete(shop_id: Optional[str] = None, ad_id: Optional[str] = None):
    cnx = connector.connect(user='root', password='psw123', port='6603', host=host, database=database)
    cursor = cnx.cursor()
    if shop_id and ad_id:
        query = "DELETE FROM phones WHERE shop_id = %s AND ad_id = %s"
        values = (shop_id, ad_id)
        execute(cursor, query, values)
        
    elif shop_id:
        query = "DELETE FROM phones WHERE shop_id = %s"
        values = (shop_id,)
        execute(cursor, query, values)
        
    elif ad_id:
        query = "DELETE FROM phones WHERE ad_id = %s"
        values = (ad_id,)
        execute(cursor, query, values)
        
    else:
        query = "DELETE FROM phones"
        execute(cursor, query)
        update_cud(cursor, 'number_of_deleted')
        cnx.commit()
        res = {"status": True, "message": "Đã xóa hết dữ liệu"}
        cnx.close()
        return res
    
    
    res = {"status": True, "message": "Xóa thành công"}
    
    update_cud(cursor, 'number_of_deleted')
    cnx.commit()
    
    cnx.close()
    return res

run(app, host="0.0.0.0", port=9002)