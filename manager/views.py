from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse

from menu.models import Category, Dish, Table

import uuid
import json


class Home(View):
    def post(self, request):
        if request.is_ajax():
            json_table = request.POST.get('table', '')

            json_dec = json.decoder.JSONDecoder()
            table = json_dec.decode(json_table)

            curr_table = Table.objects.get(pk=table)
            curr_table.url = uuid.uuid4()

            orders_list = []
            curr_table.confirmed_orders = json.dumps(orders_list)
            curr_table.unconfirmed_orders = json.dumps(orders_list)
            curr_table.save()

            context = {'tables': 'please'}
            return JsonResponse(context, status=200)

    def get(self, request):
        tables = Table.objects.all()
        return render(request, 'manager/home.html', {'tables': tables})


class NewCategory(CreateView):
    model = Category
    template_name = 'manager/category_form.html'
    fields = ('category', )

    def get_success_url(self):
        return reverse('new_category')


class NewDish(CreateView):
    model = Dish
    template_name = 'manager/dish_form.html'
    fields = ('name', 'ingredients', 'quantity', 'price', 'category', 'image')

    def get_success_url(self):
        return reverse('new_dish')


class Dishes(ListView):
    model = Dish
    context_object_name = 'dishes'


class DashboardDish(View):
    def get(self, request, *args, **kwargs):
        view = Dishes.as_view(
            template_name='manager/dashboard_dish.html',
        )

        return view(request, *args, **kwargs)


class EditDish(UpdateView):
    model = Dish
    template_name = 'manager/edit_dish.html'
    fields = ('name', 'ingredients', 'quantity', 'price', 'category', 'image', )

    def get_success_url(self):
        return reverse('dashboard')


class DeleteDish(DeleteView):
    model = Dish
    template_name = 'manager/dish_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')
