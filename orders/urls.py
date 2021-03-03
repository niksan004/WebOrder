from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:random_url>', views.CustomerOrdersView.as_view(), name='customer'),
    path('confirm_orders', views.ConfirmOrdersView.as_view(), name='confirm_orders'),
    path('cancel_order', views.CancelOrderView.as_view(), name='cancel_order'),
    path('remove_ingredient', views.RemoveIngredient.as_view(), name='remove_ingredient'),
    path('cooks', views.CooksOrdersView.as_view(), name='cooks'),
    path('done_cooks_orders', views.DoneCooksOrdersView.as_view(), name='done_cooks_orders'),
    path('distribute', views.DistributeOrdersView.as_view(), name='distribute'),
    path('dist_done', views.DistDoneView.as_view(), name='dist_done'),
]
