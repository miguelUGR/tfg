#imagen de la que nos basamos
FROM python:3.8-alpine
MAINTAINER miguel arredondo 

#variables de entorno
ENV web_dic=/aplicacion  
ENV PYTHONUNBUFFERED 1
#copia desde tu ordenador hasta la maquina virtual 
#ponemos las cosas de python
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#documento lo siguiente pk en el docker-compose, monto el directorio aplicaciones en el contenedor docker y es relevante hacer COPY
# Run, lo puedo indicar aqui o en el docker-compose

#RUN mkdir $web_dic
WORKDIR $web_dic
#COPY .$web_dic $web_dic  

RUN adduser -D user
USER user