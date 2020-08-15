from .forms import *
from .models import *
from .decorators import unauthenticated_user

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    context = {'form': form}
    return render(request, 'user/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('back', pk=user.id)
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')


def home(request):
    events = Event.objects.all().order_by('-date_created')

    context = {'events': events}
    return render(request, 'user/homepage.html', context)


def about(request):
    return render(request, 'user/about.html')


def gallary(request):
    return render(request, 'user/gallary.html')


def signup(request):
    return render(request, 'user/signup.html')


def allevents(request):
    events = Event.objects.all().order_by('-date_created')

    context = {'events': events}
    return render(request, 'user/viewevents.html', context)


def donatemoney(request):
    return render(request, 'user/donatemoney.html')


def donatebelongings(request):
    return render(request, 'user/donatebelongings.html')


@login_required(login_url='/login')
def createevent(request):

    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/allevents')

    context = {'form': form}
    return render(request, 'user/createevent.html', context)


@login_required(login_url='/login')
def orghome(request, pk):
    organization = Organization.objects.get(id=pk)
    events = organization.event_set.all()
    event_count = events.count()
    context = {'organization': organization,
               'events': events, 'event_count': event_count}
    return render(request, 'user/organizationhomepage.html', context)


def singleevent(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    return render(request, 'user/eventdet.html', context)


@login_required(login_url='/login')
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
def update_event(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        bar = event.organization_name.id
        return redirect('back', pk=bar)
    context = {'event': event}
    return render(request, 'user/delete_event.html', context)
