from django.shortcuts import render

def google_login(request):
    """
    Google Auth Page
    """
    return render(request, 'oauth/google_login.html')