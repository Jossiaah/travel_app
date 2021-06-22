from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import *

# Create your views here.


def index(request):
    if 'uuid' in request.session:
        return redirect('/dashboard')

    return render(request, 'index.html')


def register(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')
    else:
        hashing = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashing
        )
        request.session['uuid'] = new_user.id

        return redirect('/dashboard')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])

        request.session['uuid'] = user.id

        return redirect('/dashboard')


def logout(request):
    del request.session['uuid']

    return redirect('/')


def dashboard(request):
    if 'uuid' not in request.session:
        return redirect('/')

    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'all_trips': Trip.objects.all(),
        'all_users': User.objects.all(),
    }

    return render(request, 'dashboard.html', context)


def new_trip(request):
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
    }
    return render(request, 'new_trip.html', context)


def create_trip(request):
    errors = Trip.objects.new_trip_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/trips/new')
    else:
        user_logged_in = User.objects.get(id=request.session['uuid'])
        Trip.objects.create(
            destination=request.POST['destination'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            plan=request.POST['plan'],
            user=user_logged_in
        )
        return redirect('/dashboard')


def edit_trip(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'user_logged_in': User.objects.get(id=request.session['uuid']),
    }
    return render(request, 'edit.html', context)


def update_trip(request, trip_id):
    errors = Trip.objects.new_trip_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect(f'/trips/edit/{trip_id}')
    else:
        trip = Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.save()

        return redirect('/dashboard')


def trip_view(request, trip_id):
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'trip': Trip.objects.get(id=trip_id),
    }
    return render(request, 'view.html', context)


def delete_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/dashboard')
