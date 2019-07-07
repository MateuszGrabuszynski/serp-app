FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD . /code
RUN pip install pipenv
RUN pipenv install --system
