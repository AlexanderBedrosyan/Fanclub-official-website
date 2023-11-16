from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum

# func - register
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# func - login
from django.contrib.auth import authenticate, login, logout
from .models import Product, CartItem, Order, AnnualSubscriptionCards, CardItem
from django.db.models import F


# Create your views here.


def home(request):
    return render(request, 'home/home.html')

def initiatives(request):
    return render(request, 'home/initiatives.html')

def events(request):
    return render(request, 'home/events.html')

def cards(request):
    cards = AnnualSubscriptionCards.objects.all().filter()
    context = {
        'cards': cards,
    }
    return render(request, 'home/cards.html', context)

def add_new_card(request, card_id):
    # Проверка дали потребителят е логнат
    if request.user.is_authenticated:
        card = AnnualSubscriptionCards.objects.get(pk=card_id)
        cart_item, created = CardItem.objects.get_or_create(user=request.user, product=card)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cards')  # Връщаме се към страницата на магазина

    else:
        return redirect('login')  # Потребителят не е логнат, препращаме го към страницата за вход

def view_card(request):
    card_items = CardItem.objects.filter(user=request.user)
    total_amount = 0
    for card_item in card_items:
        total_amount += card_item.quantity * card_item.product.price
    context = {'cart_items': card_items, 'total_amount': total_amount}
    return render(request, 'home/view_cart.html', context)



def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'home/register.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect!')
    context = {}
    return render(request, 'home/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def store(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, "home/store.html", context)


#Cart creation
def add_to_cart(request, product_id):
    total_quantity = 0
    products = Product.objects.all()
    # Проверка дали потребителят е логнат
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id,)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
            total_quantity = cart_item.quantity
        context = {
            'total_quantity': total_quantity,
            'products': products,
        }
        return render(request, "home/store.html", context)  # Връщаме се към страницата на магазина

    else:
        return redirect('login')  # Потребителят не е логнат, препращаме го към страницата за вход

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = 0
    for cart_item in cart_items:
        total_amount += cart_item.quantity * cart_item.product.price
    context = {'cart_items': cart_items, 'total_amount': total_amount}
    return render(request, 'home/view_cart.html', context)

def checkout(request):
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')

        # Създаване на поръчката
        order = Order(user=request.user, delivery_address=delivery_address, total_price=0)

        # Запазете поръчката в базата данни
        order.save()

        total_price = 0  # Общата сума на поръчката

        # Проверка на наличността на артикулите и достатъчно количество
        for cart_item in CartItem.objects.filter(user=request.user):
            if cart_item.product.stock < cart_item.quantity:
                return render(request, 'home/view_cart.html',
                              {'error_message': 'Not enough stock for ' + cart_item.product.product_name})

            # Добавяне на поръчаните артикули към поръчката
            total_price += cart_item.quantity * cart_item.product.price
            order.ordered_items.add(cart_item)

            # Намаление на количеството на артикулите в наличност
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
            order.description += f'{cart_item.product} - {cart_item.product.price}$ - {cart_item.quantity}\n'

        # Обновяване на общата сума на поръчката
        order.total_price = total_price
        order.save()

        # Изчистване на съдържанието на кошницата на потребителя
        CartItem.objects.filter(user=request.user).delete()

        return redirect('home')  # Пренасочваме потребителя към страницата на магазина след финализация на поръчката

    return render(request, 'home/checkout.html')