from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse

from .models import Dish, Table, Category

import json


class Menu(ListView):
    model = Dish
    template_name = 'menu/menu.html'
    context_object_name = 'dishes'

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
        categories = Category.objects.all()

        context['random_url'] = self.random_url
        context['current_table'] = self.current_table
        context['categories'] = categories
        return context


class SendUncOrders(View):
    def post(self, request):
        if request.is_ajax():
            order_id_ser = request.POST.get("order_id", "")
            order_table = request.POST.get("order_table", "")

            current_table = Table.objects.get(pk=order_table)

            json_dec = json.decoder.JSONDecoder()

            prev_unc_orders = json_dec.decode(current_table.unconfirmed_orders)
            order_id = json_dec.decode(order_id_ser)

            final_unc_orders = prev_unc_orders + order_id

            current_table.unconfirmed_orders = json.dumps(final_unc_orders)
            current_table.save()

            return JsonResponse({'new_order': order_id}, status=200)
