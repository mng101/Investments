from django.core.files.base import ContentFile
from django.shortcuts import render

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DetailView)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from . import forms
from .forms import StockForm
from .models import Stock
from django.db.models import F

from io import BytesIO
from PIL import ImageGrab
import datetime

# Create your views here.

# class HomePageView(TemplateView):
#     template_name = "stocks/home.html"
#     print("HomePageView")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class HomePageView(ListView):
    model = Stock
    # paginate_by = 20
    template_name = "stocks/home.html"
    context_object_name = "stocks"
    print("test")


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "stocks/signup.html"


class ThanksPageView(TemplateView):
    template_name = 'stocks/logout.html'


class StockCreateView(CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'stocks/stock_form.html'

    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.valid = True
        return super(StockCreateView, self).form_valid(form)


class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "stocks/stock_detail.html"
    context_object_name = "Stock"


# List the Symbols in the database sorted by the "last_baystreet_entry" date to help
# identify Symbols that may potentially need to be reviewed and updated
#
class BayStreetEntryList(ListView):
    model = Stock
    # stocks = Stock.objects.all().order_by(-F('last_baystreet_entry'))
    template_name = 'stocks/baystreet_entry_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # Get the list of Stocks in the database sorted by the last_baystreet_entry date.
        # This helps identify Stocks where the Analyst Ratings may need to be updated
        #
        stocks = Stock.objects.all().order_by('last_baystreet_entry')
        return stocks


class AnalystEntryList(ListView):
    model = Stock
    # stocks = Stock.objects.all().order_by(-F('last_baystreet_entry'))
    template_name = 'stocks/analyst_entry_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # Get the list of Stocks in the database sorted by the last_baystreet_entry date.
        # This helps identify Stocks where the Analyst Ratings may need to be updated
        #
        stocks = Stock.objects.all().order_by('last_analyst_entry')
        return stocks


class ExDivDateList(ListView):
    model = Stock
    # stocks = Stock.objects.all().order_by(-F('last_baystreet_entry'))
    template_name = 'stocks/ex_div_date_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # Get the list of Stocks in the database sorted by the last_baystreet_entry date.
        # This helps identify Stocks where the Analyst Ratings may need to be updated
        #
        stocks = Stock.objects.all().order_by('ex_div_date')
        return stocks


# Refresh Analyst Ratings for the Stock from the Image captured from the Investment web site
# Analyst ratings are captured from 2 different web sites and saved with other details of the Stock
# The date when the Anlayst Rating was refreshed is also captured
#
def refresh(request,*args, **kwargs):
    print("Refreshing Image")
    clipboard = ImageGrab.grabclipboard()

    if clipboard != "None":
        symbol = kwargs["symbol"]
        img = kwargs["img"]

        stock = Stock.objects.get(symbol=symbol)

        temp_img = BytesIO()
        clipboard.save(temp_img, format="PNG", optimize=True)
        temp_img.seek(0)
        new_image = f"{symbol}_{img}.png"
        print("New Image", new_image)

        if (img == 1):
            stock.img1 = new_image
            stock.img1_refreshed_on = datetime.date.today()
            stock.img1.save(new_image, ContentFile(temp_img.read()), save=False)
        else:
            if (img == 2):
                stock.img2 = new_image
                stock.img2_refreshed_on = datetime.date.today()
                stock.img2.save(new_image, ContentFile(temp_img.read()), save=False)

        stock.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
