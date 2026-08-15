from django.core.files.base import ContentFile
from django.shortcuts import render

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DetailView)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404

from . import forms
from .forms import StockForm, PortfolioForm, HoldingForm
from .models import Stock, Portfolio, Holding
from . import utils
from django.db.models import F

from io import BytesIO
from PIL import ImageGrab
import datetime
import time

# Create your views here.


class HomePageView(ListView):
    model = Stock
    template_name = "stocks/home.html"
    context_object_name = "stocks"


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
    template_name = "stocks/holding_form.html"

    def form_valid(self, form):
        # form.instance.portfolio_name = self.kwargs['pk']
        form.instance.portfolio_name = Portfolio.objects.get(portfolio_name=self.kwargs['pk'])
        form.instance.valid = True
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the HoldingListView after successful Holding input
        return reverse('holdinglist', kwargs={'pk': self.kwargs['pk']})


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


class HoldingListView(ListView):
    model = Holding
    template_name = 'stocks/holdings_list.html'
    context_object_name = 'holdings'

    def get_queryset(self):
        holdings = Holding.objects.filter(portfolio_name=self.kwargs['pk'])

        """
        Enrich the Holdings with the current price, and 52week and target price range. This will help determine 
        if the stock is a hold or sell.
        """
        # combined_list = utils.enrich(self.request, holdings)

        return holdings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
            Add calculated fields to the context
        """

        # if context["holdings"] is not None:
        #     for item in context["holdings"]:
        #         # print(item.symbol)
        #         item["gain"] = (item.symbol.prev_close - item.avg_cost)

        # for item in context:
        #     try:
        #         item.update(
        #             {"gain": (item["symbol"]["prev_close"] - item.avg_cost)}
        #
        #         )
        #     except:
        #         pass

        return context


class HoldingUpdateView(UpdateView):
    model = Holding
    form_class = HoldingForm
    template_name = 'stocks/holding_form.html'
    context_object_name = 'holding'

    def get_object(self, queryset=None):
        # ("Getting object")
        holding = Holding.objects.get(portfolio_name=self.kwargs["portfolio"], symbol=self.kwargs["symbol"])
        return holding

    def get_success_url(self):
        # Redirect to the HoldingListView after successful Holding update
        # print("get_success_url")
        return reverse('holdinglist', kwargs={'pk': self.kwargs['portfolio']})


def holding_remove(request, **kwargs):
    """
    Remove the selected item from the list of Holdings
    """
    try:
        item = Holding.objects.get(id=kwargs['pk'])
        item.delete()
    except Holding.DoesNotExist:
        raise Http404("Holding does not exist")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Refresh Analyst Ratings for the Stock from the Image captured from the Investment web site
# Analyst ratings are captured from 2 different web sites and saved with other details of the Stock
# The date when the last Anlayst Rating was updated is also captured
#
def refresh(request, *args, **kwargs):
    # print("Refreshing Image")
    clipboard = ImageGrab.grabclipboard()

    if clipboard != "None":
        symbol = kwargs["symbol"]
        img = kwargs["img"]

        stock = Stock.objects.get(symbol=symbol)

        temp_img = BytesIO()
        clipboard.save(temp_img, format="PNG", optimize=True)
        temp_img.seek(0)
        new_image = f"{symbol}_{img}.png"
        # print("New Image", new_image)

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


# Update all Stocks in the database with market data retrieved from the Yahoo Finance API. This operations is to be
# triggered weekly to limit the number of requests being made to the API.
#
def market_data(request, *args, **kwargs):
    #
    # Get a list of Stocks recorded in the database. Limit to the first 10 during the pilot phase
    # all_stocks = Stock.objects.exclude(api_data="Y")
    all_stocks = Stock.objects.all()

    # For each item in the list combine the symbol and the exchange to create the symbol format
    # suitable for the Yahoo Finance API. Call the utils.get_quotes utility to fetch quotes for each symbol

    for item in all_stocks:
        if item.exchange is not None:
            full_symbol = item.symbol + item.exchange
            region = "CA"
        else:
            full_symbol = item.symbol
            region = "US"

        print("Quote for " + full_symbol + " " + region)

        quote = utils.get_quotes(request, region, full_symbol)

        # Update the Stock record with the data retrieved from the API
        #
        if quote:
            # print(item.symbol + "Data Retrieved")
            try:
                item.prev_close = quote[0]["regularMarketPrice"]
            except KeyError:
                print("KeyError regularMarketPrice")
                pass
            try:
                item.high52w = quote[0]["fiftyTwoWeekHigh"]
            except KeyError:
                pass
            try:
                item.low52w = quote[0]["fiftyTwoWeekLow"]
            except KeyError:
                pass
            try:
                item.target_high = quote[0]["targetPriceHigh"]
            except KeyError:
                pass
            try:
                item.target_low = quote[0]["targetPriceLow"]
            except KeyError:
                pass

            # Compute the position of the Stock, in the 52week trading range, and in relation to the targetPriceHigh.
            # These values are only calculated when market data is refreshed from RapidAPI. These values help
            # determine when the position should be partially or completely closed to realize the profit
            #
            # try:
            #     item.trading = ((quote[0]["regularMarketPrice"] - quote[0]["fiftyTwoWeekLow"])
            #                     / (quote[0]["fiftyTwoWeekHigh"] - quote[0]["fiftyTwoWeekLow"])) * 100
            # except ZeroDivisionError:
            #     pass
            # except KeyError:
            #     pass
            #
            # try:
            #     # item.target = ((quote[0]["regularMarketPrice"] - quote[0]["targetPriceLow"])
            #     #                / (quote[0]["targetPriceHigh"] - quote[0]["targetPriceLow"])) * 100
            #     item.target = ((quote[0]["regularMarketPrice"] / quote[0]["targetPriceHigh"])) * 100
            # except ZeroDivisionError:
            #     pass
            # except KeyError:
            #     pass

            try:
                item.dividend_yield = quote[0]["dividendYield"]
            except KeyError:
                pass

            try:
                item.dividend_rate = quote[0]["dividendRate"]
            except KeyError:
                pass

            try:
                date_obj = datetime.datetime.fromtimestamp(quote[0]["exDividendDate"]).date()
                item.ex_div_date = date_obj
            except KeyError:
                pass

            # Save the Stock record
            #
            item.save()
        else:
            print("No quote " + item.symbol)

    time.sleep(1)
    print("done")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
