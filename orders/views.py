from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse

from .models import CooksOrders, DistributionOrders
from menu.models import Dish, Table, Allergen
from graphs.models import DishesByPopularity
from accounts.models import User
from graphs.models import EmployeeWorkingHours

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import cook_required, distributor_required

import json
import datetime


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
        ing = []
        for order in unc_orders_list:
            d = Dish.objects.get(pk=order)
            unconfirmed_ordered_dishes.append(d)
            price += d.price

        if d is not object:
            ing = d.ingredients.split(", ")
            ing.append('--')

        # Stacking reappearing orders
        unc_orders_stacked = []

        for order in set(unconfirmed_ordered_dishes):
            unc_orders_stacked.append([order, unconfirmed_ordered_dishes.count(order)])

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

        # Stacking reappearing orders
        c_orders_stacked = []

        for order in set(confirmed_ordered_dishes):
            c_orders_stacked.append([order, confirmed_ordered_dishes.count(order)])

        # Setting up context
        context = {
            'unconfirmed_orders': unc_orders_stacked,
            'confirmed_orders': c_orders_stacked,
            'price': price,
            'current_table': self.current_table,
            'random_url': self.random_url,
            'ingredients': ing,
        }

        return context


class ConfirmOrdersView(View):
    def post(self, request):
        if request.is_ajax():
            # Confirm orders
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

            # Add orders to POPULARITY statistics
            if (
                DishesByPopularity.objects.exists() and
                datetime.datetime.now().day == DishesByPopularity.objects.latest('id').datetime.day and
                datetime.datetime.now().month == DishesByPopularity.objects.latest('id').datetime.month and
                datetime.datetime.now().year == DishesByPopularity.objects.latest('id').datetime.year
            ):
                number_of_orders = json_dec.decode(DishesByPopularity.objects.latest('id').number_of_orders)

                list_of_ids = [dish.id for dish in Dish.objects.all()]

                for ord_id in list_of_ids:
                    if ord_id in list(number_of_orders.keys()):
                        number_of_orders[ord_id] = 0

                for order in unc_orders:
                    for key, value in number_of_orders.items():
                        if int(order) == int(key):
                            number_of_orders[key] += 1

                number_of_orders_ser = json.dumps(number_of_orders)

                DishesByPopularity.objects.latest('id').delete()

                graphs_obj = DishesByPopularity()
                graphs_obj.number_of_orders = number_of_orders_ser
                graphs_obj.save()

                return JsonResponse({'new_order': unc_orders}, status=200)

            else:
                list_of_ids = [dish.id for dish in Dish.objects.all()]
                number_of_orders = {ord_id: 0 for ord_id in list_of_ids}

                for order in unc_orders:
                    for key, value in number_of_orders.items():
                        if int(order) == key:
                            number_of_orders[key] += 1

                number_of_orders_ser = json.dumps(number_of_orders)

                graphs_obj = DishesByPopularity()
                graphs_obj.number_of_orders = number_of_orders_ser
                graphs_obj.save()

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
            request.session[0] = option
            return JsonResponse({'message': 'success'}, status=200)


@method_decorator([login_required, cook_required], name='dispatch')
class CooksOrdersView(View):
    def get(self, request):
        orders_obj = CooksOrders.objects.latest('id')

        json_dec = json.decoder.JSONDecoder()
        orders_ids = json_dec.decode(orders_obj.orders)

        orders = []
        for order_id in orders_ids:
            orders.append(Dish.objects.get(pk=order_id[1]))

        orders = zip(orders, orders_ids)

        # Setting up context
        context = {
            'orders': orders,
        }
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

        # Add orders to EMPLOYEE statistics
        if (
            EmployeeWorkingHours.objects.exists() and
            datetime.datetime.now().day == EmployeeWorkingHours.objects.filter(user=request.user).latest('id').datetime.day and
            datetime.datetime.now().month == EmployeeWorkingHours.objects.filter(user=request.user).latest('id').datetime.month and
            datetime.datetime.now().year == EmployeeWorkingHours.objects.filter(user=request.user).latest('id').datetime.year
        ):
            user_log = EmployeeWorkingHours.objects.filter(user=request.user).latest('id')
            user_log.number_of_orders = user_log.number_of_orders + 1
            user_log.save()
        else:
            user_log = EmployeeWorkingHours.create(User.objects.get(pk=request.user.id))
            user_log.number_of_orders = user_log.number_of_orders + 1
            user_log.save()

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
