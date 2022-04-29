FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./backend/requirements.txt /app/
RUN  pip install -r requirements.txt
COPY ./backend/ /app/
