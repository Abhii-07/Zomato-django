from django.shortcuts import render, redirect

menu = {
    1: {'name': 'Pizza', 'price': 10, 'availability': False},
    2: {'name': 'Burger', 'price': 5, 'availability': False},
    3: {'name': 'Paneer Tikka', 'price': 8, 'availability': False},
    4: {'name': 'Chicken Biryani', 'price': 12, 'availability': True},
    5: {'name': 'Masala Dosa', 'price': 6, 'availability': True},
    6: {'name': 'Samosa', 'price': 3, 'availability': True},
    7: {'name': 'Butter Chicken', 'price': 11, 'availability': True},
    8: {'name': 'Aloo Paratha', 'price': 4, 'availability': True},
    9: {'name': 'Chole Bhature', 'price': 7, 'availability': True},
    10: {'name': 'Dal Makhani', 'price': 9, 'availability': True},
    11: {'name': 'Gulab Jamun', 'price': 3, 'availability': True},
    12: {'name': 'Rajma Chawal', 'price': 6, 'availability': True},
    13: {'name': 'Pani Puri', 'price': 4, 'availability': True},
    14: {'name': 'Pav Bhaji', 'price': 5, 'availability': True},
    15: {'name': 'Tandoori Roti', 'price': 2, 'availability': True},
}


orders = {}
order_count = 0

def home_view(request):
    context = {'home': home}
    return render(request, 'zomato_app/home.html', context)

def menu_view(request):
    context = {'menu': menu}
    return render(request, 'zomato_app/menu.html', context)



def add_dish(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = float(request.POST['price'])
        availability = request.POST.get('availability', False)
        menu[len(menu) + 1] = {'name': name, 'price': price, 'availability': availability}
        return redirect('menu')
    return render(request, 'zomato_app/add_dish.html')

def remove_dish(request, dish_id):
    if dish_id in menu:
        del menu[dish_id]
    return redirect('menu')

def update_availability(request, dish_id):
    if dish_id in menu:
        menu[dish_id]['availability'] = not menu[dish_id]['availability']
    return redirect('menu')

def take_order(request):
    global order_count
    order_count += 1
    order_id = order_count
    context = {'menu': menu, 'order_id': order_id}
    
    if request.method == 'POST':
        order = {'order_id': order_id, 'customer_name': request.POST['customer_name'], 'dishes': []}
        
        for dish_id in request.POST.getlist('selected_dishes'):
            if str(dish_id) in menu:
                if menu[dish_id]['availability']:
                    order['dishes'].append(menu[dish_id])
                else:
                    context['error_message'] = f"The dish '{menu[dish_id]['name']}' is not available for ordering."
                    return render(request, 'zomato_app/take_order.html', context)
        
        orders[order_id] = order
        return redirect('review_orders')
    
    return render(request, 'zomato_app/take_order.html', context)



def update_order_status(request, order_id):
    if order_id in orders:
        if request.method == 'POST':
            new_status = request.POST['new_status']
            orders[order_id]['status'] = new_status
            return redirect('review_orders')
    return redirect('review_orders')

def review_orders(request):
    context = {'orders': orders}
    return render(request, 'zomato_app/review_orders.html', context)

def exit_system(request):
    global orders
    orders = {}  # Clear orders when exiting
    return redirect('menu')
