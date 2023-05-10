from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('addcustomer', views.AddCustomer, name="addcustomer"),
    path('addinvoice', views.AddInvoice, name="addinvoice"),
    path('delete/<int:pk>', views.delete, name="delete"),
    path('viewinvoice/<int:pk>', views.ViewInvoice, name="viewinvoice"),
    path('invoicepdf/<int:pk>', views.InvoicePdf, name="invoicepdf"),
]