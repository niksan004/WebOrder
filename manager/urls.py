from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='manager_home'),
    path('home/check/update', views.CheckUpdate.as_view(), name='check_update'),
    path('new/category', views.NewCategory.as_view(), name='new_category'),
    path('new/dish', views.NewDish.as_view(), name='new_dish'),
    path('new/tables', views.NewTables.as_view(), name='new_tables'),
    path('QR', views.DisplayQR.as_view(), name='display_qr'),
    path('dashboard', views.DashboardDish.as_view(), name='dashboard'),
    path('dashboard/edit/<int:pk>', views.EditDish.as_view(), name='edit_dish'),
    path('dashboard/delete/<int:pk>', views.DeleteDish.as_view(), name='delete_dish'),
]