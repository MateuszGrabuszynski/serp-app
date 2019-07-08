from django.urls import path

from serp_app import views

urlpatterns = [
    path('normal_search/', views.NormalQueryView.as_view(), name='normal_query'),
    path('searches/<int:pk>', views.QueryResults.as_view(), name='search_results')
]