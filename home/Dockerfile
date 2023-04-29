FROM python:3.11-alpine
WORKDIR /home

COPY . /home
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
EXPOSE 8000
CMD ["python", "app.py"]
