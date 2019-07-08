from django.urls import path

from serp_app import views

urlpatterns = [
    path('search/', views.NormalQueryView.as_view(), name='normal_query'),
    path('latest/', views.LatestSearchesView.as_view(), name='latest_searches'),
    path('search/<int:pk>', views.QueryResults.as_view(), name='search_results'),
    path('search/<str:task_id>', views.QueryResultsByTask.as_view(), name='search_results_by_task')
]