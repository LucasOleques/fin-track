import calendar
from decimal import Decimal
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounts.models import Account
from transactions.models import Transaction


def base_view(request):
    if not request.user.is_authenticated:
        return render(request, 'apps/user/login.html')
    else:
        return redirect('dashboard')
    
@login_required
def dashboard_view(request):
    base_accounts = Account.objects.filter(user=request.user).order_by('name')
    active_accounts = base_accounts.filter(is_active=True).count()

    today = timezone.now().date()
    is_filtered = 'date_from' in request.GET or 'date_to' in request.GET

    if is_filtered:
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
    else:
        first_day_month = today.replace(day=1)
        _, num_days = calendar.monthrange(today.year, today.month)
        last_day_month = today.replace(day=num_days)

        date_from = first_day_month.strftime('%Y-%m-%d')
        date_to = last_day_month.strftime('%Y-%m-%d')

    base_transactions = Transaction.objects.filter(user=request.user)
    if date_from:
        base_transactions = base_transactions.filter(date__gte=date_from)
    if date_to:
        base_transactions = base_transactions.filter(date__lte=date_to)

    account_period_balances = base_transactions.values('account_id').annotate(
        period_income=Coalesce(Sum('value', filter=Q(transaction_type='receita')), Decimal('0.0')),
        period_expense=Coalesce(Sum('value', filter=Q(transaction_type='despesa')), Decimal('0.0'))
    ).annotate(
        period_balance=F('period_income') - F('period_expense')
    )
    balance_map = {item['account_id']: item['period_balance'] for item in account_period_balances}

    for account in base_accounts:
        account.period_balance = balance_map.get(account.pk, Decimal('0.0'))

    calc_transactions = base_transactions.exclude(account__type='poupanca')
    transactions = base_transactions.order_by('-date')[:10]

    period_income = calc_transactions.filter(transaction_type='receita').aggregate(Sum('value'))['value__sum'] or Decimal('0.00')
    period_expenses = calc_transactions.filter(transaction_type='despesa').aggregate(Sum('value'))['value__sum'] or Decimal('0.00')

    total_balance = period_income - period_expenses

    context = {
        'accounts': base_accounts,
        'total_balance': total_balance,
        'active_accounts': active_accounts,
        'transactions': transactions,
        'period_income': period_income,
        'period_expenses': period_expenses,
        'date_from': date_from,
        'date_to': date_to,
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
