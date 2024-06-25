from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('decrypt/', views.decrypt_file_view, name='decrypt_file'),
]
