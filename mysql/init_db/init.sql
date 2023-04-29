CREATE DATABASE PHONES CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
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

CREATE TABLE shops(
    shop_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (shop_id)
);
insert into cud values (0, 0, 0);

insert into shops values ('143820887');
insert into shops values ('139931303');
insert into shops values ('128013841');
insert into shops values ('142445059');
insert into shops values ('132053691');
insert into shops values ('138953767');
insert into shops values ('144157887');
insert into shops values ('144985040');