from django.shortcuts import render
from django.views.generic import View, ListView

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from .models import DishesByPopularity, EmployeeWorkingHours
from menu.models import Dish
from accounts.models import User

import json


class AboutDishes(View):
    def get(self, request):
        json_dec = json.decoder.JSONDecoder()

        data = list(json_dec.decode(DishesByPopularity.objects.latest('id').number_of_orders).values())

        dish_names = []
        for key in list(json_dec.decode(DishesByPopularity.objects.latest('id').number_of_orders).keys()):
            dish_names.append(Dish.objects.get(pk=int(key)).name)

        fig = plt.figure(figsize=(8, 3))

        ax = fig.add_subplot(facecolor='#efefef')

        ax.bar(dish_names, data)

        for axis in [ax.yaxis]:
            axis.set_major_locator(ticker.MaxNLocator(integer=True))

        fig.patch.set_facecolor('#efefef')

        fig.savefig('graphs/static/graphs/dishes_by_popularity.png')

        return render(request, 'graphs/about_dishes.html')


class AboutEmployees(View):
    def get(self, request):
        names = []

        for user in User.objects.all():
            data_orders = []
            data_dates = []
            for obj in EmployeeWorkingHours.objects.filter(user=user):
                data_orders.append(obj.number_of_orders)
                data_dates.append(obj.datetime.strftime('%d-%m'))

            fig = plt.figure(figsize=(8, 3))

            ax = fig.add_subplot(facecolor='#efefef')
            ax.bar(data_dates, data_orders)
            ax.set_title(user.username)

            fig.patch.set_facecolor('#efefef')

            fig.savefig(f'graphs/static/graphs/{user.username}.png')
            names.append(f'graphs/{user.username}.png')

        context = {'names': names}

        return render(request, 'graphs/about_employees.html', context)
