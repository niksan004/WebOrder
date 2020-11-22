from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse

from menu.models import Dish, Table
from .models import CooksOrders, DistributionOrders

import json


class CustomerOrdersView(ListView):
    model = Dish
    template_name = 'orders/orders_customers.html'
    context_object_name = 'orders'

    def get(self, request, *args, **kwargs):
        self.random_url = kwargs['random_url']
        self.current_table = object
        tables = Table.objects.all()

        for table in tables:
            if str(self.random_url) == str(table.url):
                self.current_table = Table.objects.get(pk=table.id)
                return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_dec = json.decoder.JSONDecoder()

        if self.current_table.unconfirmed_orders:
            unc_orders_list = json_dec.decode(self.current_table.unconfirmed_orders)
        else:
            unc_orders_list = []

        unconfirmed_ordered_dishes = []
        price = 0

        for order in unc_orders_list:
            d = Dish.objects.get(pk=order)
            unconfirmed_ordered_dishes.append(d)
            price += d.price

        # Confirmed
        if self.current_table.confirmed_orders:
            c_orders_list = json_dec.decode(self.current_table.confirmed_orders)
        else:
            c_orders_list = []

        confirmed_ordered_dishes = []
        price = 0

        for order in c_orders_list:
            d = Dish.objects.get(pk=order)
            confirmed_ordered_dishes.append(d)
            price += d.price

        context = {
            'unconfirmed_orders': unconfirmed_ordered_dishes,
            'confirmed_orders': confirmed_ordered_dishes,
            'price': price,
            'current_table': self.current_table,
            'random_url': self.random_url
        }

        return context


class ConfirmOrdersView(View):
    def post(self, request):
        if request.is_ajax():
            order_table = request.POST.get("order_table", "")

            json_dec = json.decoder.JSONDecoder()

            current_table = Table.objects.get(pk=order_table)
            # current_table_tuple = current_table.id

            unc_orders_ser = current_table.unconfirmed_orders
            unc_orders = json_dec.decode(unc_orders_ser)

            c_orders_ser = current_table.confirmed_orders
            c_orders = json_dec.decode(c_orders_ser)

            orders = unc_orders + c_orders

            current_table.unconfirmed_orders = json.dumps([])
            current_table.confirmed_orders = json.dumps(orders)
            current_table.save()

            cooks = CooksOrders()
            cooks.orders = json.dumps(orders)
            cooks.save()

            # final_orders = []
            # for order in orders:
            #     final_orders.append((current_table_tuple, order))
            # tuple_orders = tuple(final_orders)
            #
            # dist = DistributionOrders()
            # dist.orders = tuple_orders = tuple(final_orders)
            # dist.save()

            return JsonResponse({'new_order': unc_orders}, status=200)


class CooksOrdersView(ListView):
    model = CooksOrders
    template_name = 'orders/orders_cooks.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        json_dec = json.decoder.JSONDecoder()

        orders = []

        for i in CooksOrders.objects.all():
            for order in json_dec.decode(i.orders):
                orders.append(Dish.objects.get(pk=order))

        context['orders'] = orders

        return context


class DoneCooksOrdersView(View):
    def post(self, request):
        order_table = request.POST.get("order_table", "")
