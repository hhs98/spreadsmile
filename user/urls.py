from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage),
    path('login/', views.loginPage),
    path('logout/', views.logoutUser),

    path('', views.home),
    path('about/', views.about),
    path('gallary/', views.gallary),
    path('signup/', views.signup),
    path('allevents/', views.allevents),
    path('donatemoney/', views.donatemoney),
    path('donatebelongings/', views.donatebelongings),
    path('createevent/', views.createevent),
    path('orghome/<str:pk>/', views.orghome, name="back"),
    path('adminhome/<str:pk>/', views.adminhome, name="admin"),
    path('event/<str:pk>/', views.singleevent, name="event"),
    path('create_event/', views.create_event),
    path('update_event/<str:pk>/', views.update_event),
    path('delete_event/<str:pk>/', views.delete_event),

]
