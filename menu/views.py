from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse

from .models import Dish, Table, Category, Comment

import json


class Home(View):
    def get(self, request):
        return render(request, 'menu/home.html')


class Menu(ListView):
    model = Dish
    template_name = 'menu/menu.html'
    context_object_name = 'dishes'

    def get(self, request, *args, **kwargs):
        self.random_url = kwargs['random_url']
        self.current_table = object
        tables = Table.objects.all()

        # Find table number
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

            unc_orders = json_dec.decode(current_table.unconfirmed_orders)
            order_id = json_dec.decode(order_id_ser)

            for order in order_id:
                unc_orders.append(order)

            current_table.unconfirmed_orders = json.dumps(unc_orders)
            current_table.save()

            return JsonResponse({'new_order': order_id}, status=200)


class AddComment(View):
    def post(self, request):
        if request.is_ajax():
            comment_ser = request.POST.get("comment", "")

            json_dec = json.decoder.JSONDecoder()
            comment = json_dec.decode(comment_ser)

            comment_obj = Comment()
            comment_obj.comment = comment
            comment_obj.save()

            return JsonResponse({'message': 'success'}, status=200)
