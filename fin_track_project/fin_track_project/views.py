from django.db.models import Sum
from django.shortcuts import render
from accounts.models import Account

def base_view(request):
    if not request.user.is_authenticated:
        return render(request, 'apps/user/login.html')
    else:
        return render(request, 'dashboard.html')

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

def footer_view(request):
    return render(request, 'footer.html')

def navbar_view(request):
    return render(request, 'navbar.html')

def pagination_view(request):
    return render(request, 'pagination.html')