from django.urls import path
from . import views


app_name = 'lp'
urlpatterns = [
    path('', views.index, name='index'),
    path('get-main-information-32n42n56bh67bkj45kjnk324n5/', views.get_main_information, name='get-main-information'),
]