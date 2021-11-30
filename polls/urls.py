from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/upload/', views.upload_file, name='upload'),
    # path('upload/success', views.upload_success, name='success')
    path('passed', views.passed_tests, name='passed'),
    path('failed', views.failed_tests, name='failed')
]