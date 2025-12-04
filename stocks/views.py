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
            stock.last_update_1 = datetime.date.now()
            stock.img1.save(new_image, ContentFile(temp_img.read()), save=False)
        else:
            if (img == 2):
                stock.img2 = new_image
                stock.last_update_2 = datetime.date.now()
                stock.img2.save(new_image, ContentFile(temp_img.read()), save=False)

        stock.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
