from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),
    path('about/', views.about),
    path('gallary/', views.gallary),
    path('signup/', views.signup),
    path('allevents/', views.allevents),
    path('donatemoney/', views.donatemoney),
    path('donatebelongings/', views.donatebelongings),
    # path('createevent/', views.createevent),
    path('organization/<str:pk>/', views.organization),
    path('event/<str:pk>/', views.singleevent, name="event"),
]
