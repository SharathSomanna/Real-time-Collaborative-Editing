from django.urls import path, re_path
from . import consumers
ws_urlpatterns=[
    path('ws/sc/<str:groupname>/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),

]