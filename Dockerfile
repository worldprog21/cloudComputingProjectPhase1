# FROM python:3.7

# ENV PYTHONUNBUFFERED 1
# WORKDIR /code
# COPY . /code/
# RUN pip install -r requirements.txt

FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY . /code/
RUN pip install -r requirements.txt
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# EXPOSE 8000