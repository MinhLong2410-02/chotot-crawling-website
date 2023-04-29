from dataclasses import asdict, dataclass
import requests



shop_ids = ['143820887', '139931303', '128013841', '142445059', '132053691', '138953767', '144157887', '144985040']

@dataclass
class Phone:
    ad_id: str
    shop_id: str
    region_name: str
    price: int
    price_string: str
    can_deposit: bool
    subject_content: str
    body: str
    image_url: str

def crawl(shop_id, limit=100):
    url = f'https://gateway.chotot.com/v1/public/recommender/ad?ad_id={shop_id}&similar_type=1&limit={limit}'
    data = requests.get(url).json()['data']
    final_res = []
    for d in data:
        try:
            phone_data = asdict(Phone(
                ad_id=d['ad_id'],
                shop_id=shop_id,
                region_name=d['region_name'],
                price=d['price'],
                price_string=d['price_string'],
                can_deposit=d['can_deposit'],
                subject_content=d['subject'],
                body=d['body'],
                image_url=d['image'],
            ))
            final_res.append(phone_data)
        except Exception as e:
            continue
    return final_res




def execute(cursor, query, values=None, multi=False):
    if values is None:
        cursor.execute(query, multi=multi)
    else:
        cursor.execute(query, values, multi=multi)
    result_set = cursor.fetchall()
    return result_set

def insert_to_db(cnx, data):
    cursor = cnx.cursor()
    for record in data:
        ad_id = record['ad_id']
        shop_id = record['shop_id']
        region_name = record['region_name']
        price = record['price']
        price_string = record['price_string']
        can_deposit = bool(record['can_deposit'])
        subject_content = record['subject_content']
        body = record['body']
        image_url = record['image_url']
        query = "INSERT INTO phones (ad_id, shop_id, region_name, price, price_string, can_deposit, subject_content, body, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (ad_id, shop_id, region_name, price, price_string, can_deposit, subject_content, body, image_url)

        execute(cursor, query, values)
    cnx.commit()

def insert_shop_to_db(cnx, shop_id):
    cursor = cnx.cursor()
    query = "INSERT INTO shops (shop_id) VALUES (%s)"
    values = (shop_id,)
    execute(cursor, query, values)
    cnx.commit()

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