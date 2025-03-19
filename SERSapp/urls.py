from django.contrib import admin
from django.urls import path
from SERSapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.predict_emotion, name='predict_emotion')
]