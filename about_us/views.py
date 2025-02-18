from django.shortcuts import render

from accounts.models import User


def about_us(request):
    # View for about-us page
    users = User.objects.all()
    return render(request, 'about_us.html', {'users': users})
