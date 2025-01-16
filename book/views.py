from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .models import Book, Purchase
import stripe
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'books/book_detail.html', {'book': book})

@login_required
def create_checkout_session(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': book.title,
                    },
                    'unit_amount': int(book.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payment-success/{book.id}/'),
            cancel_url=request.build_absolute_uri(f'/book/{book.slug}/'),
        )
        return redirect(session.url)
    except Exception:
        messages.error(request, 'Payment processing failed. Please try again.')
        return redirect('book_detail', slug=book.slug)

@login_required
def payment_success(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    try:
        Purchase.objects.create(
            user=request.user,
            book=book,
            stripe_payment_id='dummy_id'
        )
        messages.success(request, f'Thank you for purchasing "{book.title}"!')
    except Exception:
        messages.error(request, 'There was an error recording your purchase.')
    
    return redirect('dashboard')

@login_required
def dashboard(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    return render(request, 'books/dashboard.html', {'purchases': purchases})

@login_required
def download_book(request, book_id):
    try:
        purchase = get_object_or_404(Purchase, user=request.user, book_id=book_id)
        book = purchase.book
        
        response = HttpResponse(book.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
        return response
    except (Purchase.DoesNotExist, FileNotFoundError):
        messages.error(request, 'You do not have access to this book.')
        return redirect('dashboard')