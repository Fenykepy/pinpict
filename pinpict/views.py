from django.shortcuts import render

def home(request):
    """Home view. If user is logged in, redirect to user home page,
    else show home page.
    """

    return render(request, 'base.html')

    

