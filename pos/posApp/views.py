from pickle import FALSE
from django.http import HttpResponse
from flask import jsonify
from posApp.models import Category, Products, Sales, salesItems, Inventory, Customer
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json, sys, os
from datetime import date, datetime
from django.forms.models import model_to_dict
from django.template.loader import get_template
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404


@login_required
def checkout_modal(request):
    # Retrieve user information from the request
    user_name = request.GET.get('user', '')

    # Pass user information to the template context
    context = {'user_name': user_name}

    return render(request, 'your_checkout_modal_template.html', context)


@login_required
def inventory(request):
    inventory_data = Inventory.objects.all()
    context = {
        'page_title': 'Inventory',
        'inventory_data': inventory_data,
    }
    return render(request, 'posApp/inventory.html', context)

@login_required
def delete_inventory(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('id')
        inventory_item = get_object_or_404(Inventory, pk=inventory_id)
        inventory_item.delete()
        return HttpResponse({'status': 'success'})
    else:
        return HttpResponse({'status': 'error'})

@login_required
def additional_action(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, pk=inventory_id)
    context = {
        'inventory_item': inventory_item,
    }
    return render(request, 'posApp/additional_action.html', {'inventory_id': inventory_id})


@login_required
def inventory(request):
    inventory = Inventory.objects.all()
    Inventory_data = []
    for inventory_item in inventory:
        data = {}
        for field in Inventory._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(inventory_item, field.name)
        data['items'] = inventory_item.objects.filter(inventory_id=inventory_item).all()
        data['item_count'] = len(data['items'])
        Inventory_data.append(data)

    # Additional data you want to pass to the template
    additional_data = "Hello from Django!"

    context = {
        'page_title': 'Inventory',
        'Inventory_data': Inventory_data,
        'additional_data': additional_data,  # Add this line
    }
    return render(request, 'posApp/inventory.html', context)

# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''} 
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")    
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total',flat=True))
    context = {
        'page_title':'Home',
        'categories' : categories,
        'products' : products,
        'transaction' : transaction,
        'total_sales' : total_sales,    

    }
    return render(request, 'posApp/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'posApp/about.html',context)

#Categories
@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title':'Category List',
        'category':category_list,
    }
    return render(request, 'posApp/category.html',context)
@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()
    
    context = {
        'category' : category
    }
    return render(request, 'posApp/manage_category.html',context)

@login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'], description = data['description'],status = data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_category(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title':'Product List',
        'products':product_list,
    }
    return render(request, 'posApp/products.html',context)

@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'posApp/manage_product.html',context)
def test(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'posApp/test.html',context)
@login_required
def save_product(request):
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def pos(request):
    products = Products.objects.filter(status = 1)
    product_json = []
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price)})
    context = {
        'page_title' : "Rey-Emily POS",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html',context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'posApp/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST

    try:
        # Get or create customer based on the logged-in user
        customer, created = Customer.objects.get_or_create(user=request.user)

        # Update customer information with the values from the form
        customer.customer_name = data.get('customer_name', '')
        customer.customer_number = data.get('customer_number', '')
        customer.payment_method = data.get('payment_method', '')  # Add this line to store payment_method
        customer.save()

        pref = datetime.now().year + datetime.now().year
        i = 1

        while Sales.objects.filter(code=str(pref) + '{:0>5}'.format(i)).exists():
            i += 1

        code = str(pref) + '{:0>5}'.format(i)

        sales = Sales(
            code=code,
            sub_total=data['sub_total'],
            tax=data['tax'],
            tax_amount=data['tax_amount'],
            grand_total=data['grand_total'],
            tendered_amount=data['tendered_amount'],
            amount_change=data['amount_change'],
            amount_balance=data['amount_balance'],
            customer=customer
        )
        sales.save()
        sale_id = sales.pk
        total_qty = 0

        for i, prod in enumerate(data.getlist('product_id[]')):
            product_id = prod
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            
            # Calculate total_qty dynamically by summing up quantities for all items
            total_qty += int(qty)

            salesItems(sale_id=sale, product_id=product, qty=qty, price=price, total=float(qty) * float(price)).save()

        # Update the total_qty for the sale
        sales.total_qty = total_qty
        sales.save()

        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        resp['total_qty'] = total_qty
        messages.success(request, "Sale Record has been saved.")

    except Exception as e:
        resp['msg'] = f"An error occurred: {str(e)}"
        print("Unexpected error:", str(e))

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def salesList(request):
    sales = Sales.objects.all()
    sale_data = []

    for sale in sales:
        data = {}
        total_qty = 0  # Initialize a variable to store the total quantity

        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)

        data['items'] = salesItems.objects.filter(sale_id=sale).all()

        for item in data['items']:
            total_qty += item.qty  # Add qty for each item to the total quantity

        data['total_qty'] = total_qty  # Add total_qty to data

        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')

        sale_data.append(data)

    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
    }

    return render(request, 'posApp/sales.html', context)

@login_required
def collection(request):
    sales = Sales.objects.all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']),'.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html',context)


# Corrected code
@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    

    if sales is not None:
        transaction = model_to_dict(sales)

        # Retrieve customer name and number
        try:
            transaction['customer_name'] = sales.customer.customer_name
            transaction['customer_number'] = sales.customer.customer_number
            transaction['total_qty'] = sales.total_qty
            transaction['payment_method'] = sales.customer.payment_method
        except AttributeError:
            # Handle the case where total_qty attribute is not found
            transaction['total_qty'] = 0  # Provide a default value or handle it as needed

        # Format tax amount if present
        if 'tax_amount' in transaction:
            transaction['tax_amount'] = format(float(transaction['tax_amount']))

        ItemList = salesItems.objects.filter(sale_id=sales).all()

        context = {
            "transaction": transaction,
            "salesItems": ItemList,
        }

        template = get_template('posApp/receipt.html')
        html = template.render(context)

        return HttpResponse(html)
    else:
        # Handle the case where no sales with the given ID is found
        return HttpResponse("Sales not found.")

@login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')