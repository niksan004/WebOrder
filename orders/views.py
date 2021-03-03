from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse

from menu.models import Dish, Table
from .models import CooksOrders, DistributionOrders

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import cook_required, distributor_required

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

        # Unconfirmed
        if self.current_table.unconfirmed_orders:
            unc_orders_list = json_dec.decode(self.current_table.unconfirmed_orders)
        else:
            unc_orders_list = []

        unconfirmed_ordered_dishes = []
        price = 0

        d = object
        for order in unc_orders_list:
            d = Dish.objects.get(pk=order)
            unconfirmed_ordered_dishes.append(d)
            price += d.price

        ing = d.ingredients.split(", ")
        ing.append('--')

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
            'random_url': self.random_url,
            'ingredients': ing,
        }

        return context


class ConfirmOrdersView(View):
    def post(self, request):
        if request.is_ajax():
            order_table = request.POST.get("order_table", "")

            json_dec = json.decoder.JSONDecoder()

            current_table = Table.objects.get(pk=order_table)
            current_table_tuple = current_table.id

            unc_orders_ser = current_table.unconfirmed_orders
            unc_orders = json_dec.decode(unc_orders_ser)

            c_orders_ser = current_table.confirmed_orders
            c_orders = json_dec.decode(c_orders_ser)

            orders = unc_orders + c_orders

            current_table.unconfirmed_orders = json.dumps([])
            current_table.confirmed_orders = json.dumps(orders)
            current_table.save()

            final_orders = []
            for order in orders:
                final_orders.append((current_table_tuple, order))
            tuple_orders = tuple(final_orders)

            cooks = CooksOrders()
            cooks.orders = json.dumps(tuple_orders)
            cooks.save()

            return JsonResponse({'new_order': unc_orders}, status=200)


class CancelOrderView(View):
    def post(self, request):
        if request.is_ajax():
            order_id_ser = request.POST.get("order_id", "")
            current_table_ser = request.POST.get("current_table", "")

            json_dec = json.decoder.JSONDecoder()

            table = Table.objects.get(pk=json_dec.decode(current_table_ser))
            order_id = json_dec.decode(order_id_ser)

            orders = json_dec.decode(table.unconfirmed_orders)
            orders.remove(order_id)

            table.unconfirmed_orders = json.dumps(orders)
            table.save()

            return JsonResponse({'message': 'success'}, status=200)


class RemoveIngredient(View):
    def post(self, request):
        if request.is_ajax():
            option = request.POST.get("option", "")
            return JsonResponse({'message': 'success'}, status=200)


@method_decorator([login_required, cook_required], name='dispatch')
class CooksOrdersView(View):
    def get(self, request):
        orders_obj = CooksOrders.objects.latest('id')

        json_dec = json.decoder.JSONDecoder()
        orders_ids = json_dec.decode(orders_obj.orders)

        print(orders_ids)

        orders = []
        for order_id in orders_ids:
            orders.append(Dish.objects.get(pk=order_id[1]))

        orders = zip(orders, orders_ids)

        context = {'orders': orders}
        return render(request, 'orders/orders_cooks.html', context)


class DoneCooksOrdersView(View):
    def post(self, request):
        done_order_id = request.POST.get("done_order_id", "")

        json_dec = json.decoder.JSONDecoder()

        orders = json_dec.decode(CooksOrders.objects.latest('id').orders)

        for index, order in enumerate(orders):
            if int(order[1]) == int(json_dec.decode(done_order_id)):
                del orders[index]
                break

        cooks = CooksOrders.objects.latest('id')
        cooks.orders = json.dumps(orders)
        cooks.save()

        return JsonResponse({'message': 'success'}, status=200)


@method_decorator([login_required, distributor_required], name='dispatch')
class DistributeOrdersView(View):
    def post(self, request):
        id_table_ser = request.POST.get("id_table", "")

        json_dec = json.decoder.JSONDecoder()
        id_table = json_dec.decode(id_table_ser)

        id_table_list = []
        id_table_list.append(id_table[1])
        id_table_list.append(id_table[5])

        distributors = DistributionOrders.objects.latest('id')
        orders = [i for i in json_dec.decode(distributors.orders)]

        orders.append(id_table_list)

        distributors.orders = json.dumps(orders)
        distributors.save()

        return JsonResponse({'message': 'success'}, status=200)

    def get(self, request):
        distributors = DistributionOrders.objects.latest('id')
        json_dec = json.decoder.JSONDecoder()
        orders_ids = [i for i in json_dec.decode(distributors.orders)]

        orders = []
        tables = []
        for order_id in orders_ids:
            orders.append(Dish.objects.get(pk=order_id[1]))
            tables.append(order_id[0])

        orders = zip(orders, tables)

        context = {'orders': orders}

        return render(request, 'orders/orders_distribution.html', context)


@method_decorator([login_required, distributor_required], name='dispatch')
class DistDoneView(View):
    def post(self, request):
        id_order_ser = request.POST.get("order_done", "")
        id_table_ser = request.POST.get("table_done", "")

        json_dec = json.decoder.JSONDecoder()
        id_order = json_dec.decode(id_order_ser)
        id_table = json_dec.decode(id_table_ser)

        distribute_obj = DistributionOrders.objects.latest('id')
        orders = [i for i in json_dec.decode(distribute_obj.orders)]

        for index, pair in enumerate(orders):
            if pair[0] == id_table and pair[1] == id_order:
                del orders[index]
                break

        distribute_obj.orders = json.dumps(orders)
        distribute_obj.save()

        return JsonResponse({'message': 'success'}, status=200)
