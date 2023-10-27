# FROM python:3.10-slim

FROM python:alpine

RUN pip install --upgrade pip


WORKDIR /user/src/

COPY ./requirements.txt /user/src/
RUN python3 -m pip install -r requirements.txt
COPY . /user/src/



# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]


