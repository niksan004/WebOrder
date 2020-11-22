from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:random_url>', views.CustomerOrdersView.as_view(), name='customer'),
    path('confirm_orders', views.ConfirmOrdersView.as_view(), name='confirm_orders'),
    path('cooks_orders', views.CooksOrdersView.as_view(), name='cooks_orders'),
    path('done_cooks_orders', views.DoneCooksOrdersView.as_view(), name='done_cooks_orders'),
]
