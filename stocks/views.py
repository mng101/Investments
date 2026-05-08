from django.core.files.base import ContentFile
from django.shortcuts import render

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DetailView)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from . import forms
from .forms import StockForm, PortfolioForm, HoldingForm
from .models import Stock, Portfolio, Holding
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
    # print("test")


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

    def form_valid(self, form):
        form.instance.valid = True
        return super(StockCreateView, self).form_valid(form)


class PortfolioCreateView(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    success_url = reverse_lazy("portfoliolist")
    template_name = 'stocks/portfolio_form.html'


class HoldingCreateView(CreateView):
    model = Holding
    form_class = HoldingForm
    # success_url = reverse_lazy("holdingslist")
    template_name = "stocks/holding_form.html"

    # def get_initial(self):
    #     print("Get Initial")
    #     # initial = {'portfolio_name': Portfolio.objects.get(portfolio_name = self.kwargs['pk'])}
    #     return {'portfolio_name': Portfolio.objects.get(portfolio_name = self.kwargs['pk'])}
    #     # return self.initial.copy()

    # def get_form_kwargs(self):
    #     kwargs = super(HoldingCreateView, self).get_form_kwargs()
    #     # kwargs.update({'portfolio_name': self.request.pk})
    #     return kwargs

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     # kwargs.update({'portfolio_name': self.kwargs.pk})
    #     # kwargs['portfolio_name'] = self.kwargs.get('pk')
    #     # kwargs['pk'] = self.kwargs.get('pk')
    #     return kwargs

    def form_valid(self, form):
        # form.instance.portfolio_name = self.kwargs['pk']
        form.instance.portfolio_name = Portfolio.objects.get(portfolio_name = self.kwargs['pk'])
        form.instance.valid = True
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the HoldingListView after successful Holding input
        return reverse('holdingslist', kwargs={'pk': self.kwargs['pk']})


class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "stocks/stock_detail.html"
    context_object_name = "Stock"


class PortfolioUpdateView(UpdateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'stocks/portfolio_form.html'
    context_object_name = "Portfolio"


# List the Symbols in the database sorted by the "last_baystreet_entry" date to help
# identify Symbols that may potentially need to be reviewed and updated
#
class BayStreetEntryList(ListView):
    model = Stock
    template_name = 'stocks/baystreet_entry_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # Get the list of Stocks in the database sorted by the last_baystreet_entry date.
        # This helps identify Stocks where the Analyst Ratings may need to be updated
        #
        stocks = Stock.objects.annotate(
            data=F('last_baystreet_entry')
        ).values('symbol', 'data').order_by('data')
        return stocks


class AnalystEntryList(ListView):
    model = Stock
    # stocks = Stock.objects.all().order_by(-F('last_baystreet_entry'))
    template_name = 'stocks/analyst_entry_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # Get the list of Stocks in the database sorted by the last_analyst_entry.
        # This helps identify Stocks where the Analyst Ratings may need to be updated
        #
        stocks = Stock.objects.annotate(
            data=F('last_analyst_entry')
        ).values('symbol', 'data').order_by('data')
        return stocks


class ExDivDateList(ListView):
    model = Stock
    # stocks = Stock.objects.all().order_by(-F('last_baystreet_entry'))
    template_name = 'stocks/ex_div_date_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # Get the list of Stocks in the database sorted by the ex_div_date.
        # This helps identify Stocks where the Ex_Div_Date may need to be updated
        #
        stocks = Stock.objects.annotate(
            data=F('ex_div_date')
        ).values('symbol', 'data').order_by('data')
        return stocks


class GenericList(ListView):
    # This is a Generic List View that can be used as a template for other lists
    # that display the Symbol and ONLY one other data element
    # The data element listed for the Symbol is annotated as 'data' in the QuerySet to
    # support a generic template for the list
    model = Stock
    template_name = 'stocks/generic_list.html'
    context_object_name = "stocks"

    def get_queryset(self):
        # This is a sample QuerySet to support the Generic List function
        # Replace the 'last_baystreet_entry' with the desired data element
        #
        stocks = Stock.objects.annotate(
            data=F('last_baystreet_entry')
            ).values('symbol', 'data', ).order_by('data')
        return stocks


class PortfolioListView(ListView):
    model = Portfolio
    template_name = "stocks/portfolio_list.html"
    context_object_name = "portfolio"

    def get_queryset(self):
        portfolio = Portfolio.objects.order_by("portfolio_name")
        return portfolio

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["portfolio"] = Portfolio.objects.order_by("portfolio_name")
    #     return context


class HoldingListView(ListView):
    model = Holding
    template_name = 'stocks/holdings_list.html'
    context_object_name = 'holdings'

    def get_queryset(self):
        holdings = Holding.objects.filter(portfolio_name=self.kwargs['pk'])
        return holdings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["portfolio"] = Portfolio.objects.order_by("portfolio_name")
        return context


# Refresh Analyst Ratings for the Stock from the Image captured from the Investment web site
# Analyst ratings are captured from 2 different web sites and saved with other details of the Stock
# The date when the Anlayst Rating was refreshed is also captured
#
def refresh(request, *args, **kwargs):
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

        if img == 1:
            stock.img1 = new_image
            stock.img1_refreshed_on = datetime.date.today()
            stock.img1.save(new_image, ContentFile(temp_img.read()), save=False)
        else:
            if img == 2:
                stock.img2 = new_image
                stock.img2_refreshed_on = datetime.date.today()
                stock.img2.save(new_image, ContentFile(temp_img.read()), save=False)

        stock.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
