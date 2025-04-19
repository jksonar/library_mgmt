from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from .models import Book
from django.db.models import Count
from django.utils.dateparse import parse_date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Issue
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Book, Issue
from django.contrib.admin.views.decorators import staff_member_required

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books, 'query': query})

@login_required
def issue_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.quantity <= 0:
        messages.warning(request, f"'{book.title}' is out of stock and cannot be issued.")
        return redirect('book_list')

    if request.method == 'POST':
        duration = request.POST.get('duration')
        if duration == 'monthly':
            return_date = timezone.now().date() + timedelta(days=30)
        elif duration == 'quarterly':
            return_date = timezone.now().date() + timedelta(days=90)
        else:  # annually
            return_date = timezone.now().date() + timedelta(days=365)

        Issue.objects.create(user=request.user, book=book, return_date=return_date)
        book.quantity -= 1
        book.save()
        messages.success(request, f'{book.title} issued for {duration}.')
        return redirect('my_books')

    return render(request, 'library/issue_duration.html', {'book': book})


@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id, user=request.user)
    book = issue.book
    book.quantity += 1
    book.save()
    issue.delete()
    messages.success(request, f"You have returned {book.title}.")
    return redirect('my_books')

@login_required
def my_books(request):
    issues = Issue.objects.filter(user=request.user)
    return render(request, 'library/my_books.html', {'issues': issues})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'library/dashboard.html')


@staff_member_required
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    total_issued = Issue.objects.count()
    available_books = Book.objects.filter(quantity__gt=0).count()
    recent_issues = Issue.objects.select_related('book', 'user').order_by('-issue_date')[:5]

    # Filtering by date (optional)
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    issued_books_qs = Issue.objects.all()

    if start_date and end_date:
        issued_books_qs = issued_books_qs.filter(issue_date__range=[start_date, end_date])

    # Books per category for chart
    category_data = Book.objects.values('category__name').annotate(total=Count('id'))
    categories = [item['category__name'] for item in category_data]
    category_counts = [item['total'] for item in category_data]

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_issued': total_issued,
        'available_books': available_books,
        'recent_issues': recent_issues,
        'categories': categories,
        'category_counts': category_counts,
        'start_date': start_date,
        'end_date': end_date,
        'issued_books_qs': issued_books_qs
    }
    return render(request, 'library/admin_dashboard.html', context)

def landing_page(request):
    return render(request, 'library/landing.html')


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

# views.py
from django.contrib.auth.views import LogoutView

class LogoutViaGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
