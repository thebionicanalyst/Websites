from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('skillset/', views.dashboard_view, name='skillset'),
    path('streamlit/', views.streamlit_view, name='streamlit'),
    path('projects/', views.portfolio_view, name='projects'),
]