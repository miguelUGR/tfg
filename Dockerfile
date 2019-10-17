FROM python:3.8-alpine
MAINTAINER miguel arredondo 

ENV web_dic=/aplicacion  
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir $web_dic
WORKDIR $web_dic
COPY .$web_dic $web_dic

RUN adduser -D user
USER user