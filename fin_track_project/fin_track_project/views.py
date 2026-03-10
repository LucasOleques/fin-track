from django.shortcuts import render

def base_view(request):
    if not request.user.is_authenticated:
        return render(request, 'apps/user/login.html')
    else:
        return render(request, 'dashboard.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def footer_view(request):
    return render(request, 'footer.html')

def navbar_view(request):
    return render(request, 'navbar.html')

def pagination_view(request):
    return render(request, 'pagination.html')