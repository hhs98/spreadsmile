from .forms import *
from .models import *
from django.contrib.auth.models import User, Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# for payment

import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.save()

            group = Group.objects.get(name='organizations')
            user.groups.add(group)
            Organization.objects.create(
                user=user,
                orgname=user.username,
            )

            return redirect('/login')
    context = {'form': form}
    return render(request, 'user/registration.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin', pk=user.id)
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form)
        print(form.is_valid())
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'user/register.html', context)


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


def donatemoney(request, pk):
    event = Event.objects.get(id=pk)
    form = MoneyDonatorForm(initial={'event': event.id})
    if request.method == 'POST':
        form = MoneyDonatorForm(request.POST)
        if form.is_valid():
            form.save()
            donator = MoneyDonatorInfo.objects.get(name=request.POST.get(
                'name'), email=request.POST.get('email'), contact=request.POST.get('contact'))
            return redirect('pay', pk=donator.id)
    context = {'form': form}
    return render(request, 'user/donatemoney.html', context)


def payment(request, pk):
    store_id = 'spere5f3aeaafa6b1d'
    api_key = 'spere5f3aeaafa6b1d@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True,
                            sslc_store_id=store_id, sslc_store_pass=api_key)

    status_url = request.build_absolute_uri(reverse("status"))

    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    donator = MoneyDonatorInfo.objects.get(id=pk)
    donate_amount = donator.amount
    mypayment.set_product_integration(total_amount=Decimal(donate_amount), currency='BDT', product_category='donation',
                                      product_name='Donate Money', num_of_item=1, shipping_method='None', product_profile='None')

    mypayment.set_customer_info(name=donator.name, email=donator.email, address1='demo address 1',
                                address2='demo address 2', city='Dhaka', postcode='1200', country='Bangladesh', phone=donator.contact)

    mypayment.set_shipping_info(shipping_to=donator.name, address='demo address',
                                city='Dhaka', postcode='1200', country='Bangladesh')

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(
                request, 'Your Donation has been Completed Successfully, Redirecting to home page...')
        elif status == 'FAILED':
            messages.warning(
                request, 'Your Donation has been Failed, Please try again, Redirecting to home page...')
    context = {}
    return render(request, 'user/complete.html', context)


def donatebelongings(request):
    return render(request, 'user/donatebelongings.html')


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def orghome(request, pk):
    organization = Organization.objects.get(id=pk)
    events = organization.event_set.all()
    event_count = events.count()
    context = {'organization': organization,
               'events': events, 'event_count': event_count}
    return render(request, 'user/organizationhomepage.html', context)


@login_required(login_url='/login')
@admin_only
def adminhome(request, pk):
    user = User.objects.get(id=pk)
    inactive_users = User.objects.filter(is_active=False)
    context = {'user': user, 'inactive_users': inactive_users}
    return render(request, 'user/adminhomepage.html', context)


def singleevent(request, pk):
    event = Event.objects.get(id=pk)
    donators = event.moneydonatorinfo_set.all()

    donators_count = donators.count()
    if(donators_count == 0):
        raised = 0
        raised_p = 0
        context = {'event': event,
                   'donators_count': donators_count, 'raised': raised, 'raised_p': raised_p}
        return render(request, 'user/eventdet.html', context)
    else:
        get_total = donators.aggregate(Sum('amount'))
        raised = get_total['amount__sum']
        raised_p = (get_total['amount__sum']/event.goal)*100
        context = {'event': event,
                   'donators_count': donators_count, 'raised': raised, 'raised_p': raised_p}
        return render(request, 'user/eventdet.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
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
@allowed_users(allowed_roles='organizations')
def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        bar = event.organization_name.id
        return redirect('back', pk=bar)
    context = {'event': event}
    return render(request, 'user/delete_event.html', context)
