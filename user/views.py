from django.shortcuts import render, redirect

from .models import *
from .forms import *

# Create your views here.


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


# def createevent(request):

#     form = EventForm()

#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('/allevents')

#     context = {'form': form}
#     return render(request, 'user/createevent.html', context)


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
