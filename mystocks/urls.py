"""mytstocks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="myStocks/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("thanks/", views.ThanksPageView.as_view(), name="thanks"),
    path("stocks/", views.StockCreateView.as_view(), name="stocks"),
    path("stocks/<int:pk>/", views.StockUpdateView.as_view(), name="update"),
    # path("stocks/<str:symbol>/", views.TestUpdateView.as_view(), name="test"),
]
