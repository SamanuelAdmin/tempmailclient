FROM python:3.12.8-alpine3.20

WORKDIR /temp_mail_client

ADD . /temp_mail_client

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]