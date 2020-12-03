from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import OrderForm
import sweetify


def home(request):
    list_custumer = Custumer.objects.all()
    list_order = Order.objects.all()
    total_orders = list_order.count()
    delivered = list_order.filter(status='Delivered').count()
    pending = list_order.filter(status='Pending').count()

    context = {
        'judul': 'Halaman Beranda',
        'menu': 'home',
        'custumer': list_custumer,
        'order': list_order,
        'data_total_orders': total_orders,
        'data_delivered': delivered,
        'data_pending': pending,
    }
    return render(request, 'masruri/dashboard.html', context)


def products(request):
    list_product = Product.objects.all()

    context = {
        'judul': 'Halaman Produk',
        'menu': 'products',
        'product': list_product,
    }
    return render(request, 'masruri/products.html', context)


def custumer(request, pk):
    detailcustumer = Custumer.objects.get(id=pk)
    order_custumer = detailcustumer.order_set.all()
    total_custumer = order_custumer.count()
    context = {
        'judul': 'Halaman Konsumen',
        'custumer': detailcustumer,
        'data_order_custumer': order_custumer,
        'data_total_custumer': total_custumer,
    }
    return render(request, 'masruri/custumer.html', context)


def createOrder(request):
    formorder = OrderForm()
    if request.method == 'POST':
        # print('Cetak POST:', request.POST)
        formsimpan = OrderForm(request.POST)
        if formsimpan.is_valid:
            formsimpan.save()
            sweetify.success(
                request, 'You did it', text='Good job! You successfully showed a SweetAlert message', persistent='Hell yeah')
            return redirect('/')

    context = {
        'judul': 'Form Order',
        'form': formorder,
    }
    return render(request, 'masruri/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    formorder = OrderForm(instance=order)
    if request.method == 'POST':
        # print('Cetak POST:', request.POST)
        formedit = OrderForm(request.POST, instance=order)
        if formedit.is_valid:
            formedit.save()
            return redirect('/')

    context = {
        'judul': 'Edit Order',
        'form': formorder,
    }
    return render(request, 'masruri/order_form.html', context)


def deleteOrder(request, pk):
    orderhapus = Order.objects.get(id=pk)
    if request.method == 'POST':
        orderhapus.delete()
        return redirect('/')

    context = {
        'judul': 'Hapus Data Order',
        'dataorderdelete': orderhapus,
    }
    return render(request, 'masruri/delete_form.html', context)
