from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Tip
from .forms import TipForm

def redirect_to_home(request):
    return redirect('home')

class HomePageView(View):
    def get(self, request):
        tips = Tip.objects.all().order_by('-date')
        form = TipForm() if request.user.is_authenticated else None
        return render(request, 'home.html', {
            'tips': tips,
            'form': form,
            'username': request.user.username if request.user.is_authenticated else request.defaultName
        })

    def post(self, request):
        if request.user.is_authenticated:
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()
        return redirect('home')

@login_required(login_url='/login')
def upvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user in tip.downvotes.all():
        tip.downvotes.remove(request.user)
    if request.user in tip.upvotes.all():
        tip.upvotes.remove(request.user)
    else:
        tip.upvotes.add(request.user)
    tip.author.update_reputation()
    return redirect('home')

@login_required(login_url='/login')
def downvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user == tip.author or request.user.can_downvote():
        if request.user in tip.upvotes.all():
            tip.upvotes.remove(request.user)
        if request.user in tip.downvotes.all():
            tip.downvotes.remove(request.user)
        else:
            tip.downvotes.add(request.user)
        tip.author.update_reputation()
    else:
        return HttpResponseForbidden("You don't have permission to downvote this tip.")
    return redirect('home')

@login_required(login_url='/login')
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user == tip.author or request.user.can_delete_tips():
        tip.delete()
    else:
        return HttpResponseForbidden("You don't have permission to delete this tip.")
    return redirect('home')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html', {
            'username': request.defaultName
        })

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
        return render(request, 'login.html', {
            'username': request.defaultName
        })

class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'registration.html', {'username': request.defaultName})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        username = request.POST['username']
        password = request.POST['pass']
        password_confirm = request.POST['secur_pass']

        User = get_user_model()

        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
        elif not username:
            messages.error(request, 'Empty username field')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'registration.html', {'username': "Guest"})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')