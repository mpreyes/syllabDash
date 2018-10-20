
from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('show_file_contents/', views.show_file_contents, name='show_file'),
    path('list_assignments/', views.list_assignments, name='list_assignments'),
    path('finished_upload/', views.finished_upload, name='finished_upload'),
]

