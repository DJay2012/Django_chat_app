from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.models import Message
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def index(request):  # Define a view function for the root URL
    return redirect('chat')

@login_required
def chat(request, user_id=None):
    users = User.objects.all()
    receiver = None
    messages = Message.objects.none()

    if user_id:
        receiver = get_object_or_404(User, id=user_id)
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
        ).order_by('timestamp')

    return render(request, 'chat.html', {'receiver': receiver, 'messages': messages, 'users': users})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages  # Import messages

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully!')  # Add success message
            return redirect('login')  # Redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')  # Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})