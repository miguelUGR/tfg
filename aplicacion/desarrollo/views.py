from django.shortcuts import render

# Create your views here.
def hola(request , nombre): #tiene dos parameteos el request para coger datos y el nombre que le pasamos <>
    return render (request,"hola.html",{'nombre': nombre}) # nos vamos ha hola.html 