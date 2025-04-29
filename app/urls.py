from django.urls import path,include # type: ignore
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('client/home/', views.client_home, name='client_home'),
    path('responsable_home/', views.respo_home, name='responsabel_home'),
    path('technicien_home/', views.technicien_home, name='technicien_home'),
]