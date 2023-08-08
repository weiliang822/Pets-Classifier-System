from django.urls import path, include

from . import views

urlpatterns = [
    path("pets_classify/", views.petsClassify, name='pets_classify'),
]
