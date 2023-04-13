from django.urls import path
from . import views


app_name = 'admin_panel'
urlpatterns = [
    path('client-dfn23423nroi2rvi32inc23px3p23ppm2/', views.clients, name='clients'),
    path('delete-client-adjn23jnjcn234c3m54cp34mmp/<str:phone_number>/', views.delete_client, name='delete-client'),
    path('main-information-j2nnl453k4vn3o4n534c343/', views.main_information, name='main-information'),
    path('add-main-information-anj23j2nc3n423nc233/', views.add_main_information, name='add-main-information'),
    path('delete-main-information-po23pjp23po2c323/', views.delete_main_information, name='delete-main-information'),
    path('add-media-23n2b4iu4hco34icp34pii34ncn3c4/', views.add_media, name='add-media'),
    path('delete-media-2j3n23cm4mc34nc3434c34pm34o/', views.delete_media, name='delete-media'),
    path('add-book-2342534c34pp3c4p3j4vpjij4cir3pi/', views.add_book, name='add-book'),
    path('delete-book-jn34jn4kc34b5jc43nlk6778m987/', views.delete_book, name='delete-book'),
    path('add-faq-jndkjfgnkdjf3234h4n5v85v09j92jv9/', views.add_faq, name='add-faq'),
    path('delete-daq-3i4pooij3pn34i6in6n756jn7n78n/', views.delete_faq, name='delete-faq'),
]