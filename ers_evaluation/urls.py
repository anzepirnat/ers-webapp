from django.urls import path

from . import views

#app_name = "ers_evaluation"
urlpatterns = [
    path("", views.index, name="index"),
    path("evaluation/", views.evaluation, name="evaluation"),
    path("result/", views.result, name="result"),
    path('delete_evaluation/', views.delete_evaluation, name='delete_evaluation'),
    path("evaluation/edit/", views.edit_evaluation, name="edit_evaluation"),
]