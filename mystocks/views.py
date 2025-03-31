from django.shortcuts import render

from django.shortcuts import render

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DetailView)

from . import forms
from .forms import StockForm
from .models import Stock

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


class StockCreateView(CreateView):
    model = Stock
    form_class = StockForm
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.valid = True
        return super(StockCreateView, self).form_valid(form)


class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "mystocks/stock_form.html"
    context_object_name = "Stock"

    # def get_context_data(self, **kwargs):
    #     # context = super(StockDetailView, self).get_context_data(**kwargs)
    #     context = Stock.objects.get(id=self.kwargs['id'])
    #     return context

# class TestUpdateView(UpdateView):
#     model = Stock
#     form_class = StockForm
#     template_name = "mystocks/stock_form.html"
#     context_object_name = "Stock"