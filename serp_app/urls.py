from django.urls import path

from serp_app import views

urlpatterns = [
    path('normal/', views.NormalQueryView.as_view(), name='normal_query'),
    path('results/<int:pk>', views.QueryResults.as_view(), name='query_results')
]