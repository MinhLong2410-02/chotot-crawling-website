import mysql.connector as connector
def init_db():
    host = "host.docker.internal"
    port = '6603'
    database = 'PHONES'

    cnx = connector.connect(user='root', password='psw123', port=port, host=host, database=database)
    cursor = cnx.cursor()
    query = '''
        USE PHONES;
        show tables;        
    '''
    data = cursor.execute(query, multi=True)
    data = cursor.fetchall()
    print(data)
    # query = \
    #     '''
    #     USE PHONES;
    #     CREATE TABLE phones (
    #         ad_id VARCHAR(255) NOT NULL,
    #         shop_id VARCHAR(255) NOT NULL,
    #         region_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    #         price INT NOT NULL,
    #         price_string VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    #         subject_content VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    #         can_deposit TINYINT NOT NULL,
    #         body TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    #         image_url VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    #         PRIMARY KEY (ad_id)
    #     );


    #     CREATE TABLE cud(
    #         number_of_created INT NOT NULL,
    #         number_of_updated INT NOT NULL,
    #         number_of_deleted INT NOT NULL
    #     );
    #     insert into cud values (0, 0, 0);

    #     CREATE TABLE shops(
    #         shop_id VARCHAR(255) NOT NULL,
    #         PRIMARY KEY (shop_id)
    #     );
    #     insert into shops values ('143820887');
    #     insert into shops values ('139931303');
    #     insert into shops values ('128013841');
    #     insert into shops values ('142445059');
    #     insert into shops values ('132053691');
    #     insert into shops values ('138953767');
    #     insert into shops values ('144157887');
    #     insert into shops values ('144985040');
    #     '''
    # cursor.execute(query, multi=True)
    # cnx.commit()
    cnx.close()

init_db()