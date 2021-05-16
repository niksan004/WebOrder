from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required

from .models import PaidTable
from menu.models import Category, Dish, Table, QrCode, Comment

import uuid
import json


@method_decorator([login_required, admin_required], name='dispatch')
class Home(View):
    def post(self, request):
        if request.is_ajax():
            json_table = request.POST.get('table', '')

            json_dec = json.decoder.JSONDecoder()
            table = json_dec.decode(json_table)

            url = uuid.uuid4()

            curr_qr = QrCode.objects.get(pk=table)
            curr_qr.name = f'weborder.sliven.org/menu/{url}'
            curr_qr.save()

            curr_table = Table.objects.get(pk=table)
            curr_table.url = url
            curr_table.QR = curr_qr

            if curr_table.check != 0:
                payed_table = PaidTable()
                payed_table.bill = curr_table.check
                payed_table.save()

            orders_list = []
            curr_table.confirmed_orders = json.dumps(orders_list)
            curr_table.unconfirmed_orders = json.dumps(orders_list)
            curr_table.check = 0
            curr_table.save()

            context = {'tables': 'please'}
            return JsonResponse(context, status=200)

    def get(self, request):
        tables = Table.objects.all()
        return render(request, 'manager/home.html', {'tables': tables})


@method_decorator([login_required, admin_required], name='dispatch')
class CheckUpdate(View):
    def post(self, request):
        id_order_ser = request.POST.get("order", "")
        id_table_ser = request.POST.get("table", "")

        json_dec = json.decoder.JSONDecoder()
        id_order = json_dec.decode(id_order_ser)
        id_table = json_dec.decode(id_table_ser)

        table = Table.objects.get(pk=int(id_table))
        price = Dish.objects.get(pk=int(id_order)).price

        table.check = table.check + price
        table.save()

        return JsonResponse({'message': 'success'}, status=200)


@method_decorator([login_required, admin_required], name='dispatch')
class NewCategory(CreateView):
    model = Category
    template_name = 'manager/category_form.html'
    fields = ('title', 'title_en', )

    def get_success_url(self):
        return reverse('new_category')


@method_decorator([login_required, admin_required], name='dispatch')
class NewDish(CreateView):
    model = Dish
    template_name = 'manager/dish_form.html'
    fields = ('name', 'ingredients', 'allergens', 'quantity', 'price', 'category', 'image')

    def get_success_url(self):
        return reverse('new_dish')


@method_decorator([login_required, admin_required], name='dispatch')
class NewTables(View):
    def get(self, request):
        return render(request, 'manager/table_form.html')

    def post(self, request):
        new_QR = QrCode()
        url = uuid.uuid4()
        new_QR.name = f'weborder.sliven.org/menu/{url}'
        new_QR.save()

        new_table = Table()
        new_table.url = url
        new_table.QR = new_QR
        new_table.save()
        return JsonResponse({'message': 'success'}, status=200)


@method_decorator([login_required, admin_required], name='dispatch')
class DisplayQR(View):
    def get(self, request):
        QR = QrCode.objects.all()
        tables = Table.objects.all()
        display = zip(tables, QR)
        context = {'display': display}
        return render(request, 'manager/QR.html', context)


@method_decorator([login_required, admin_required], name='dispatch')
class Dishes(ListView):
    model = Dish
    context_object_name = 'dishes'


@method_decorator([login_required, admin_required], name='dispatch')
class DashboardDish(View):
    def get(self, request, *args, **kwargs):
        view = Dishes.as_view(
            template_name='manager/dashboard_dish.html',
        )

        return view(request, *args, **kwargs)


@method_decorator([login_required, admin_required], name='dispatch')
class EditDish(UpdateView):
    model = Dish
    template_name = 'manager/edit_dish.html'
    fields = ('name', 'ingredients', 'quantity', 'price', 'category', 'image', )

    def get_success_url(self):
        return reverse('dashboard')


@method_decorator([login_required, admin_required], name='dispatch')
class DeleteDish(DeleteView):
    model = Dish
    template_name = 'manager/dish_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


@method_decorator([login_required, admin_required], name='dispatch')
class History(View):
    def get(self, request):
        payed_tables = PaidTable.objects.order_by("datetime").reverse()
        context = {'payed_tables': payed_tables}
        return render(request, 'manager/history.html', context)


@method_decorator([login_required, admin_required], name='dispatch')
class Comments(View):
    def get(self, request):
        comments = Comment.objects.order_by("time_added")
        context = {'comments': comments}
        return render(request, 'manager/comments.html', context)
