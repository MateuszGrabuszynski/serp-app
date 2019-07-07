from django.urls import path

from serp_app import views

urlpatterns = [
    path('normal/', views.NormalQueryView.as_view(), name='normal_query')
]