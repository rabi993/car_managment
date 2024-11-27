from django.shortcuts import render, redirect,get_object_or_404
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from .models import Car, Cart, CartItem

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
# Create your views here.

@login_required
def add_car(request):
    if request.method =='POST':
        car_form = forms.CarForm(request.POST)
        if car_form.is_valid():
            car_form.instance.l_user = request.user
            car_form.save()
            return redirect('homepage')
    else:
        car_form = forms.CarForm()

    return render(request, 'add_car.html', {'form': car_form})

# Add car using Class based view
@method_decorator(login_required, name='dispatch')
class AddCarCreateView(CreateView):
    model = models.Car
    form_class= forms.CarForm
    template_name= 'add_car.html'
    # success_url= reverse_lazy('add_car')
    success_url= reverse_lazy('homepage')
    def form_valid(self, form): 
        form.instance.l_user = self.request.user
        return super().form_valid(form)



@login_required
def edit_car(request, id):
    car = models.Car.objects.get(pk=id)
    car_form = forms.CarForm(instance=car)
    # print(car.title)
    if request.method =='POST':
        car_form = forms.CarForm(request.POST, instance=car)
        if car_form.is_valid():
            car_form.instance.l_user = request.user
            car_form.save()
            return redirect('homepage')
    # else:
    #     car_form = forms.CarForm()

    return render(request, 'add_car.html', {'form': car_form})

# Edit car using class based view
@method_decorator(login_required, name='dispatch')
class EditCarView(UpdateView):
    model = models.Car
    form_class = forms.CarForm
    template_name ='add_car.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')




@login_required
def delete_car(request, id):
    car = models.Car.objects.get(pk=id)
    car.delete()
    return redirect('homepage')

# delete car using class based view
@method_decorator(login_required, name='dispatch')
class DeleteCarView(DeleteView):
    model = models.Car
    template_name ='delete.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'

class DetailCarView(DetailView):
    model = models.Car
    # pk_url_kwarg='id'
    template_name = 'car_details.html'


    def post(self, request, *args, **kwargs):
        comment_form= forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = post
            new_comment.save()
        return self.get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

# def buy_now(request, car_id):
#         car = get_object_or_404(Car, id=car_id)
#         if car.Available > 0:
#             car.decrease_available()
#             # Get or create a cart for the user
#             cart, created = Cart.objects.get_or_create(user=request.user)
            
#             # Check if item is already in the cart
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, car=car)
            
#             if not created:
#                 # If item already in cart, increment quantity
#                 cart_item.quantity += 1
#                 cart_item.save()
#         return redirect('detail_car', pk=car.id)

# def buy_now(request, car_id):
#     car = get_object_or_404(Car, id=car_id)
    
#     # Ensure the user has enough balance
#     user_account = request.user.account
#     if car.Available > 0:
#         if user_account.total_money >= car.price:
#             # Deduct the price of the car from the user's account balance
#             user_account.total_money -= car.price
#             user_account.save()

#             # Decrease car availability
#             car.decrease_available()

#             # Get or create a cart for the user
#             cart, created = Cart.objects.get_or_create(user=request.user)

#             # Check if item is already in the cart
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, car=car)

#             if not created:
#                 # If item already in cart, increment quantity
#                 cart_item.quantity += 1
#                 cart_item.save()
#             messages.success(request, "Car purchased successfully!")
#         else:
#             messages.error(request, "Insufficient balance to buy this car.")
#     else:
#         messages.error(request, "Car is not available.")
    
#     return redirect('detail_car', pk=car.id)
# from decimal import Decimal

# def buy_now(request, car_id):
#     car = get_object_or_404(Car, id=car_id)
    
#     # Ensure the user has enough balance
#     user_account = request.user.account
#     if car.Available > 0:
#         if user_account.balance >= Decimal(str(car.Price)):  # Convert car price to Decimal
#             # Deduct the price of the car from the user's account balance
#             user_account.balance -= Decimal(str(car.Price))  # Ensure balance is updated with Decimal
#             user_account.save()

#             # Decrease car availability
#             car.decrease_available()

#             # Get or create a cart for the user
#             cart, created = Cart.objects.get_or_create(user=request.user)

#             # Check if item is already in the cart
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, car=car)

#             if not created:
#                 # If item already in cart, increment quantity
#                 cart_item.quantity += 1
#                 cart_item.save()
            
#             messages.success(request, "Car purchased successfully!")
#         else:
#             messages.error(request, "Insufficient balance to buy this car.")
#     else:
#         messages.error(request, "Car is not available.")
    
#     return redirect('detail_car', pk=car.id)
from decimal import Decimal
from transactions.constants import BUY_CAR
from transactions.models import Transaction  # Import the transaction model and type

def buy_now(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Ensure the user has enough balance
    user_account = request.user.account
    if car.Available > 0:
        if user_account.balance >= Decimal(str(car.Price)):  # Convert car price to Decimal
            # Deduct the price of the car from the user's account balance
            user_account.balance -= Decimal(str(car.Price))
            user_account.save()

            # Record the transaction with type `BUY_CAR`
            Transaction.objects.create(
                account=user_account,
                amount=Decimal(str(car.Price)),
                transaction_type=BUY_CAR,
                balance_after_transaction=user_account.balance
            )

            # Decrease car availability
            car.decrease_available()

            # Get or create a cart for the user
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Check if item is already in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, car=car)

            if created:
                # If a new item is added, set its price
                cart_item.price = car.Price
            else:
                # If the item already exists, increment quantity
                cart_item.quantity += 1

            # Save the updated cart item
            cart_item.save()

            messages.success(request, "Car purchased successfully!")
        else:
            messages.error(request, "Insufficient balance to buy this car.")
    else:
        messages.error(request, "Car is not available.")

    return redirect('detail_car', pk=car.id)
