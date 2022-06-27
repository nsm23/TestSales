import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from googledata.management import (get_all_values,
                                   get_currency,
                                   get_deleted_sales)
from googledata.models import NumbersModel
from googledata.serializers import NumbersSerializer


class NumbersUpdate(APIView):
    """Create new orders or update existing"""

    def post(self, request):
        sales = get_all_values()
        currency = get_currency()
        existing_orders = NumbersModel.objects.values_list("order")

        new_orders = tuple(sale[0] for sale in sales)

        deleted_orders = get_deleted_sales(new_orders, existing_orders)

        for sale in sales:
            order, cost_usd, delivery_date = sale

            data = {
                "order": int(order),
                "cost_usd": int(cost_usd),
                "cost_rub": int(cost_usd) * currency,
                "delivery_date": datetime.date(int(delivery_date.split(".")[2]),
                                               int(delivery_date.split(".")[1]),
                                               int(delivery_date.split(".")[0]))
            }

            serializer = NumbersSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

        for order in deleted_orders:
            NumbersModel.objects.filter(order=order).delete()

        return Response(status=201)


class NumbersList(generics.ListAPIView):
    """List sales"""
    queryset = NumbersModel.objects.all()
    serializer_class = NumbersSerializer
