from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Order
from .forms import BookForm, OrderForm
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    books = Book.objects.filter(stock__gt=0)
    return render(request, 'home.html', {'books': books})

@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def order_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.book = book
            if order.quantity <= book.stock:
                order.save()
                book.stock -= order.quantity
                book.save()
                return redirect('home')
            else:
                form.add_error('quantity', 'Not enough books in stock')
    else:
        form = OrderForm(initial={'book': book})
    return render(request, 'order_book.html', {'form': form, 'book': book})

@login_required
def list_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'list_orders.html', {'orders': orders})
