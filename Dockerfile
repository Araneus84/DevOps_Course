FROM python:3.14.0b1-alpine3.21

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .

CMD python app.py


