from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounts.models import Account
from transactions.models import Transaction


def base_view(request):
    if not request.user.is_authenticated:
        return render(request, 'apps/user/login.html')
    else:
        accounts = Account.objects.filter(user=request.user)
        total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0.00
        active_accounts = accounts.filter(is_active=True).count()

        context = {
            'accounts': accounts,
            'total_balance': total_balance,
            'active_accounts': active_accounts,
            # 'recent_transactions': recent_transactions,
            'monthly_income': 0.00,
            'monthly_expenses': 0.00,
        }
        return render(request, 'dashboard.html', context)
    
@login_required
def dashboard_view(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0.00
    active_accounts = accounts.filter(is_active=True).count()
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    
    today = timezone.now().date()
    first_day_month = today.replace(day=1)
    
    monthly_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='receita',
        date__gte=first_day_month
    ).aggregate(Sum('value'))['value__sum'] or 0.00
    
    monthly_expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='despesa',
        date__gte=first_day_month
    ).aggregate(Sum('value'))['value__sum'] or 0.00

    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'active_accounts': active_accounts,
        'transactions': transactions,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
    }

    return render(request, 'dashboard.html', context)

@login_required
def footer_view(request):
    return render(request, 'components/footer.html')

@login_required
def navbar_view(request):
    return render(request, 'components/navbar.html')

@login_required
def pagination_view(request):
    return render(request, 'components/pagination.html')
