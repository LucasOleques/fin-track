from django.db.models import Sum
from django.shortcuts import render
from accounts.models import Account
from django.contrib.auth.decorators import login_required

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
def footer_view(request):
    return render(request, 'footer.html')

@login_required
def navbar_view(request):
    return render(request, 'navbar.html')

@login_required
def pagination_view(request):
    return render(request, 'pagination.html')