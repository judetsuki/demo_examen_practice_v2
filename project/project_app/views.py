from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
# Create your views here.

def delete_order(request,pk):
    if request.user.is_superuser:
        get_object_or_404(Order,pk=pk).delete()
    return redirect('product_list')

def delete_product(request,pk):
    if request.user.is_superuser:
        get_object_or_404(Product,pk=pk).delete()
    return redirect('product_list')

def edit_product(request,pk):
    if not request.user.is_superuser:
        return redirect('product_list')
    
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render (request, 'store/form_generic.html', {'form':form, 'title':'редактирование продукта'})

def edit_order(request,pk):
    if not request.user.is_superuser:
        return redirect('product_list')
    
    order = get_object_or_404(Order,pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = OrderForm(instance=order)
    return render (request, 'store/form_generic.html', {'form':form, 'title':'редактирование заказов'})


def product_list(request):
    user = request.user
    products = Product.objects.all()
    orders = []

    if user.is_authenticated and user.is_staff or user.is_superuser:
        search_query=request.GET.get('search')
        if search_query:
            products=products.filter(name__icontains=search_query)
        orders = Order.objects.all()

    return render (request, 'store/product_list.html',{
        'products': products,
        'orders': orders,
    })