from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage),
    path('login/', views.loginPage),
    path('logout/', views.logoutUser),

    path('', views.home, name="home"),
    path('about/', views.about),
    path('gallary/', views.gallary),
    path('signup/', views.signup),
    path('allevents/', views.allevents),
    path('donatemoney/<str:pk>/', views.donatemoney),
    path('payment/<str:pk>/', views.payment, name="pay"),
    path('status/', views.complete, name="status"),
    path('donatebelongings/', views.donatebelongings),
    path('orghome/<str:pk>/', views.orghome, name="back"),
    path('adminhome/<str:pk>/', views.adminhome, name="admin"),
    path('event/<str:pk>/', views.singleevent, name="event"),
    path('create_event/', views.create_event),
    path('update_event/<str:pk>/', views.update_event),
    path('delete_event/<str:pk>/', views.delete_event),

]
