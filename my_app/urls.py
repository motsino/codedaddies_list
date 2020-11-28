from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('new_search', views.new_search, name='new_search')
]
