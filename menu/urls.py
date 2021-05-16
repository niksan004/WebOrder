from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<uuid:random_url>', views.Menu.as_view(), name='menu'),
    path('send_unc_orders', views.SendUncOrders.as_view(), name='send_unc_orders'),
    path('add_comment', views.AddComment.as_view(), name='add_comment'),
]
