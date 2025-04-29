from django.urls import path # type: ignore
from django.contrib.auth.views import LogoutView # type: ignore
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('client_home/', views.client_home, name='client_home'),
    path('responsable_home/', views.respo_home, name='responsable_home'),  # Fixed name to match view
    path('technicien_home/', views.technicien_home, name='technicien_home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Add logout URL
    path('default_home/', views.default_home, name='default_home'),  # Add default home
]