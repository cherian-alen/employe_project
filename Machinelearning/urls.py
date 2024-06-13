from django.urls import path,include
from .import views

urlpatterns=[
     path('take_img',views.take_img),
     path('start_attendence',views.Fillattendances)
]