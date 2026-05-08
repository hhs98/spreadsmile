from .forms import *
from .models import *
from django.contrib.auth.models import User, Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# for payment

import uuid

import requests
from decimal import Decimal, InvalidOperation
from django.views.decorators.csrf import csrf_exempt

SSLCOMMERZ_SESSION_API_SANDBOX = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'
SSLCOMMERZ_SESSION_API_LIVE = 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'
SSLCOMMERZ_VALIDATION_API_SANDBOX = (
    'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php'
)
SSLCOMMERZ_VALIDATION_API_LIVE = (
    'https://securepay.sslcommerz.com/validator/api/validationserverAPI.php'
)


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    orgform = OrganizationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        orgform = OrganizationForm(request.POST)
        if form.is_valid() and orgform.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='organizations')
            user.groups.add(group)
            org = orgform.save(commit=False)
            org.user = user
            org.orgname = user.username
            org.orgemail = user.email
            org.save()
            return redirect('/login')
    context = {'form': form, 'orgform': orgform}
    return render(request, 'user/registration.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group_names = set(user.groups.values_list('name', flat=True))
            if 'admins' in group_names:
                return redirect('admin', pk=user.id)
            if 'organizations' in group_names:
                try:
                    return redirect('back', pk=user.organization.id)
                except Organization.DoesNotExist:
                    messages.error(
                        request,
                        'Your account has no organization profile. Contact support.',
                    )
                    return redirect('home')
            return redirect('home')
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


def allevents(request):
    events = Event.objects.all().order_by('-date_created')
    context = {'events': events}
    return render(request, 'user/viewevents.html', context)


def donatemoney(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = MoneyDonatorForm()
    if request.method == 'POST':
        form = MoneyDonatorForm(request.POST)
        if form.is_valid():
            donator = form.save(commit=False)
            donator.event = event
            donator.save()
            return redirect('pay', pk=donator.id)
    context = {'form': form}
    return render(request, 'user/donatemoney.html', context)


def payment(request, pk):
    donator = MoneyDonatorInfo.objects.get(id=pk)
    if donator.amount is None:
        messages.error(request, 'Invalid donation amount.')
        return redirect('home')

    status_url = request.build_absolute_uri(reverse('status'))
    total_amount = f'{Decimal(donator.amount):.2f}'
    # tran_id must be unique and <= 30 characters (SSLCommerz limit)
    tran_id = f'D{donator.id}-{uuid.uuid4().hex[:12]}'[:30]

    phone = (donator.contact or '')[:20]
    cus_name = (donator.name or 'Donor')[:50]
    cus_email = (donator.email or '')[:50]

    payload = {
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_passwd': settings.SSLCOMMERZ_STORE_PASSWD,
        'total_amount': total_amount,
        'currency': 'BDT',
        'tran_id': tran_id,
        'success_url': status_url,
        'fail_url': status_url,
        'cancel_url': status_url,
        'ipn_url': status_url,
        'product_category': 'donation',
        'product_name': 'Donate Money',
        'product_profile': 'non-physical-goods',
        'num_of_item': 1,
        'shipping_method': 'NO',
        'cus_name': cus_name,
        'cus_email': cus_email,
        'cus_add1': 'N/A',
        'cus_add2': '',
        'cus_city': 'Dhaka',
        'cus_state': 'Dhaka',
        'cus_postcode': '1200',
        'cus_country': 'Bangladesh',
        'cus_phone': phone or '01700000000',
        'cus_fax': phone or '01700000000',
        'ship_name': cus_name,
        'ship_add1': 'N/A',
        'ship_add2': '',
        'ship_city': 'Dhaka',
        'ship_state': 'Dhaka',
        'ship_postcode': '1200',
        'ship_country': 'Bangladesh',
        'value_a': str(donator.id),
    }

    api_url = (
        SSLCOMMERZ_SESSION_API_SANDBOX
        if settings.SSLCOMMERZ_USE_SANDBOX
        else SSLCOMMERZ_SESSION_API_LIVE
    )
    try:
        api_response = requests.post(api_url, data=payload, timeout=30)
        api_response.raise_for_status()
        response_data = api_response.json()
    except (requests.RequestException, ValueError):
        messages.error(request, 'Could not start payment. Please try again.')
        return redirect('home')

    if response_data.get('status') == 'SUCCESS' and response_data.get('GatewayPageURL'):
        return redirect(response_data['GatewayPageURL'])

    reason = response_data.get('failedreason') or response_data.get('message') or 'Unknown error'
    messages.error(request, f'Payment gateway error: {reason}')
    return redirect('home')


@csrf_exempt
def complete(request):
    context = {}
    if request.method != 'POST':
        return render(request, 'user/complete.html', context)

    post = request.POST
    status = post.get('status', '')

    if status == 'FAILED':
        messages.warning(
            request,
            'Your donation could not be completed. Please try again.',
        )
        return render(request, 'user/complete.html', context)

    if status != 'VALID':
        messages.warning(
            request,
            f'Payment was not completed (status: {status or "unknown"}).',
        )
        return render(request, 'user/complete.html', context)

    val_id = post.get('val_id')
    if not val_id:
        messages.error(request, 'Invalid payment response: missing validation id.')
        return render(request, 'user/complete.html', context)

    validation_url = (
        SSLCOMMERZ_VALIDATION_API_SANDBOX
        if settings.SSLCOMMERZ_USE_SANDBOX
        else SSLCOMMERZ_VALIDATION_API_LIVE
    )
    try:
        validation_resp = requests.get(
            validation_url,
            params={
                'val_id': val_id,
                'store_id': settings.SSLCOMMERZ_STORE_ID,
                'store_passwd': settings.SSLCOMMERZ_STORE_PASSWD,
                'format': 'json',
            },
            timeout=30,
        )
        validation_resp.raise_for_status()
        vdata = validation_resp.json()
    except (requests.RequestException, ValueError):
        messages.error(
            request,
            'Could not verify payment with SSLCommerz. If you were charged, please contact support.',
        )
        return render(request, 'user/complete.html', context)

    if vdata.get('status') != 'VALIDATED':
        messages.error(
            request,
            'Payment could not be verified. If money was deducted, please contact support.',
        )
        return render(request, 'user/complete.html', context)

    post_tran_id = post.get('tran_id', '')
    if post_tran_id and vdata.get('tran_id') != post_tran_id:
        messages.error(request, 'Transaction reference mismatch after validation.')
        return render(request, 'user/complete.html', context)

    try:
        validated_amount = Decimal(str(vdata.get('amount') or '0'))
    except (InvalidOperation, ValueError, TypeError):
        messages.error(request, 'Invalid amount in validation response.')
        return render(request, 'user/complete.html', context)

    currency = (vdata.get('currency') or '').upper()
    if currency != 'BDT':
        messages.error(request, 'Unexpected currency from payment gateway.')
        return render(request, 'user/complete.html', context)

    value_a = post.get('value_a') or vdata.get('value_a')
    if not value_a:
        messages.error(request, 'Could not match payment to a donation (missing reference).')
        return render(request, 'user/complete.html', context)

    try:
        donator = MoneyDonatorInfo.objects.get(pk=int(value_a))
    except (ValueError, TypeError, MoneyDonatorInfo.DoesNotExist):
        messages.error(request, 'Could not match this payment to a donation record.')
        return render(request, 'user/complete.html', context)

    expected = Decimal(donator.amount or 0)
    if validated_amount != expected:
        messages.error(
            request,
            'Paid amount does not match the donation. Please contact support if you were charged.',
        )
        return render(request, 'user/complete.html', context)

    messages.success(
        request,
        'Your donation has been completed successfully. Redirecting to home page...',
    )
    return render(request, 'user/complete.html', context)


def donatebelongings(request):
    return render(request, 'user/donatebelongings.html')


@login_required(login_url='/login')
@allowed_users(['organizations'])
def orghome(request, pk):
    organization = get_object_or_404(Organization, pk=pk, user=request.user)
    events = organization.event_set.all()
    event_count = events.count()
    context = {'organization': organization,
               'events': events, 'event_count': event_count}
    return render(request, 'user/organizationhomepage.html', context)


@login_required(login_url='/login')
@admin_only
def adminhome(request, pk):
    if request.user.id != int(pk):
        return HttpResponseForbidden(
            'You cannot view another user\'s dashboard.'
        )
    user = request.user
    events = Event.objects.all().order_by('-date_created')
    #inactive_users = User.objects.filter(is_active=False)
    inactive_users = Organization.objects.all().order_by('-orgdate')
    context = {'user': user, 'inactive_users': inactive_users, 'events': events}
    return render(request, 'user/adminhomepage.html', context)


@login_required(login_url='/login')
@admin_only
def apporg(request, pk):
    org = User.objects.get(id=pk)
    if request.method == 'POST':
        org.is_active = True
        org.save()
        return redirect('admin', pk=request.user.id)
    context = {'org': org}
    return render(request, 'user/approve.html', context)


@login_required(login_url='/login')
@admin_only
def deapporg(request, pk):
    org = User.objects.get(id=pk)
    if request.method == 'POST':
        org.is_active = False
        org.save()
        return redirect('admin', pk=request.user.id)
    context = {'org': org}
    return render(request, 'user/deactive.html', context)


def singleevent(request, pk):
    event = Event.objects.get(id=pk)
    donators = event.moneydonatorinfo_set.all()

    donators_count = donators.count()
    if(donators_count == 0):
        raised = 0
        raised_p = 0
        context = {'event': event,
                   'donators_count': donators_count, 'raised': raised, 'raised_p': raised_p}
        return render(request, 'user/details.html', context)
    else:
        get_total = donators.aggregate(Sum('amount'))
        raised = get_total['amount__sum']
        raised_p = (get_total['amount__sum']/event.goal)*100
        context = {'event': event,
                   'donators_count': donators_count, 'raised': raised, 'raised_p': raised_p}
        return render(request, 'user/details.html', context)


@login_required(login_url='/login')
@allowed_users(['organizations'])
def create_event(request):
    organization = get_object_or_404(Organization, user=request.user)
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization_name = organization
            event.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
@allowed_users(['organizations'])
def update_event(request, pk):
    event = get_object_or_404(
        Event,
        pk=pk,
        organization_name__user=request.user,
    )
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
@allowed_users(['organizations'])
def delete_event(request, pk):
    event = get_object_or_404(
        Event,
        pk=pk,
        organization_name__user=request.user,
    )
    if request.method == 'POST':
        org_pk = event.organization_name_id
        event.delete()
        return redirect('back', pk=org_pk)
    context = {'event': event}
    return render(request, 'user/delete_event.html', context)
