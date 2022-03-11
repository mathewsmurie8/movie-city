from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from accounts.models import BDSGUser
from movies.models import RentalRequest

def register(request):
  if request.method == 'POST':
    # Get form values
    username = request.POST['username']
    if username:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
          # Looks good
          user = User.objects.create_user(username=username)
          BDSGUser.objects.create(user=user)
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Please enter your username')
      return redirect('register')
  else:
    context = {}
    return render(request, 'accounts/register.html', context)

def login(request):
  if request.method == 'POST':
    username = request.POST['username']

    user = None
    if User.objects.filter(username=username).exists():
      user = User.objects.get(username=username)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

def dashboard(request):
  user = request.user
  rental_requests = RentalRequest.objects.filter(user=user)
  context = {
    'rental_requests': rental_requests
  }
  return render(request, 'accounts/dashboard.html', context)
