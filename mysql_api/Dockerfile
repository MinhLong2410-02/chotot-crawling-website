FROM python:3.11-alpine
WORKDIR /mysql_api
COPY . /mysql_api
RUN pip install -r requirements.txt
CMD ["python", "main.py"]