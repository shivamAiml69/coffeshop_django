from django.shortcuts import render, redirect, get_object_or_404
from .models import Coffee

def home(request):
    return render(request, 'coffee.html')

def menu(request):
    coffees = Coffee.objects.all()
    return render(request, 'coffee/menu.html', {'coffees': coffees})

def bill(request):
    items = []
    total = 0
    if request.method == 'POST':
        # Collect all selected coffees and quantities
        for key in request.POST:
            if key.startswith('coffee_id_'):
                coffee_id = request.POST[key]
                quantity = int(request.POST.get(f'quantity_{coffee_id}', 0))
                if quantity > 0:
                    coffee = get_object_or_404(Coffee, id=coffee_id)
                    amount = coffee.price * quantity
                    items.append({'coffee': coffee, 'quantity': quantity, 'amount': amount})
                    total += amount

        # If checkout button was pressed, update inventory and redirect
        if 'checkout' in request.POST:
            for item in items:
                coffee = item['coffee']
                quantity = item['quantity']
                if coffee.quantity >= quantity:
                    coffee.quantity -= quantity
                    coffee.save()
            return redirect('home')

        # Otherwise, just show the bill
        return render(request, 'coffee/bill.html', {'items': items, 'total': total})

    # GET request: show empty bill
    return render(request, 'coffee/bill.html', {'items': [], 'total': 0})


