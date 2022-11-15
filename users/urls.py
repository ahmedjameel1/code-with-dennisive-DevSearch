from django.urls import path
from . import views




urlpatterns = [
    path('', views.profiles,name = 'profiles'),
    path('userprofile/<str:pk>/', views.userProfile,name = 'user-profile'),
    path('login/', views.loginPage , name = 'login' ),
    path('loggedout/', views.logoutUser , name = 'logout' ),
    path('register/', views.registerUser , name = 'register' ),
    path('account/', views.userAccount , name = 'account'),
    path('addskill/', views.addSkill , name = 'add-skill'),
    path('editskill/<str:pk>', views.editSkill , name = 'edit-skill'),
    path('deleteskill/<str:pk>', views.deleteSkill , name = 'delete-skill'),
    path('editprofile', views.editProfile , name = 'edit-profile'),
    path('inbox', views.inbox , name = 'inbox'),
    path('viewmessage/<str:pk>/', views.viewMessage , name = 'viewmessage'),
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),






] 
