#syntax=docker/dockerfile:1

FROM python:3-alpine
WORKDIR /app
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN apk add py3-pip 
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
RUN ./manage.py makemigrations
RUN ./manage.py migrate
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

LABEL name="passman-backend"
LABEL version="1.0"
LABEL author="Sharan Varma"
LABEL author_email="sharanvarma0@gmail.com"
LABEL python_requires="3.9"

