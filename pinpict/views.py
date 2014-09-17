from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy

def home(request):
    """Home view. If user is logged in, redirect to user home page,
    else login page.
    """
    if request.user.is_authenticated():
        return redirect(reverse_lazy('boards_list',
            kwargs={
                'user': request.user.slug,
            }))
    
    return redirect(reverse_lazy('user_login'))

    

