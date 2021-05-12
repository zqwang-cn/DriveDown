from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('download/<int:id>', views.download, name='download'),
    path('get/<int:id>', views.get, name='get'),
    path('list', views.list, name='list'),
    path('confirm/<int:id>', views.confirm, name='confirm'),
]
