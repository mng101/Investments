from django.shortcuts import render

from django.shortcuts import render

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, )

from . import forms
# from .forms import StockForm
# from .models import Stock

# Create your views here.

class HomePageView(TemplateView):
    template_name = "myStocks/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "myStocks/signup.html"


class ThanksPageView(TemplateView):
    template_name = 'myStocks/logout.html'


# class StockCreateView(CreateView):
#     model = Stock
#     form_class = StockForm
#     success_url = reverse_lazy("home")
