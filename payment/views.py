from django.shortcuts import render
from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentForm
from django.views.generic import View


class Payment(View):
    def get(self, request):
        paypal_dict = {
            'business'
        }
