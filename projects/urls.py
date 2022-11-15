from django.urls import path
from . import views





urlpatterns = [
    path('', views.projects,name = 'projects'),
    path('project/<str:pk>/', views.project,name = 'project'),
    path('editproject/<str:pk>/', views.editProject,name = 'edit-project'),
    path('delproject/<str:pk>/', views.delProject,name = 'del-project'),
    path('createproject/', views.createProject,name = 'create-project'),


]
