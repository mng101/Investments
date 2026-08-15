import datetime
import json
import http.client

from django.conf import settings
from .models import Stock


def get_quotes(requests, region, symbol):
    #
    # Make API calls to retrieve quotes for securities of interest
    # For the time being, we will request quotes for only one Security at a time, and limit the request to
    # once a week
    # This can be subsequently improved to request multiple Securities in each request, with more frequent requests
    #

    conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "438c096415mshb0589791ceeff23p107e84jsnd9ed933221e3",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("GET", "/market/v2/get-quotes?region=" + region + "&symbols=" + symbol, headers=headers)

    response = conn.getresponse()

    if response.status == 200:
        data = response.read()
        json_data = json.loads(data)
        return json_data["quoteResponse"]["result"]
    else:
        return None


# def enrich(request, sym_list):
#     """
#     Given a list of items (holdings, watchlist, etc) combine the list with RapidAPI data saved in
#     the Stock model
#     :param request:
#     :param sym_list: List of symbols of interest
#     :return:
#     """
#
#     combined_list=[]
#
#     for item in sym_list:
#         symbol = Stock.objects.get(id=item['symbol_id']).symbol
#
#         print(symbol)



