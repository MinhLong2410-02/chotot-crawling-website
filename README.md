# chotot-phone-crawling-website
Simple project to crawl phone data from shops on chotot.com webstite

## Installation

Make sure to create venv before pip install 

```bash
python -m venv .venv
.venv\Scripts\active
pip install -r requirements.txt
```

## Database: MySQL
password: psw123 \
port: 6603:3306

## Docker
For first time run
```docker
docker-compose up --build
```

Before running on local, remember to host database first
```sql
HOST=localhost
PASSWORD=psw123
PORT=6603
DATABASE=PHONES
```
Run on Home folder
```bash
.venv\Scripts\active
cd Home
python app.py
```
