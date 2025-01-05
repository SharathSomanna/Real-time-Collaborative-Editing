from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name='index_no_group'),
    path('<str:group_name>/', views.index, name='index'),
]