from django.shortcuts import render, redirect, get_object_or_404

from myapp.forms import AddFlightForm
from myapp.models import Flight


# Create your views here.
def index(request):
    """Here we can get all the elements we need to show on the index page, so I choose the Flight objects"""
    flights = Flight.objects.all()
    #this is used so we can send it in the html with some kind of 'model' we used in ASP.Net
    context = {'flights':flights}
    return render(request,'index.html',context)
def object_details(request,flight_id):
    flight = Flight.objects.filter(id=flight_id).first()
    context = {'flight':flight}
    return render(request,'details.html',context)
def add_flight(request):
    if request.method == 'POST':
        form = AddFlightForm(request.POST, request.FILES)
        if form.is_valid():
            #When i want to make the user automatically, this is what needs to be done
            flight = form.save(commit=False)
            flight.user_that_created = request.user
            flight.save()
        return redirect('index')
    form = AddFlightForm()
    context = {'form':form}
    return render(request, "add_fligt_form.html",context)

def edit_flight(request,flight_id):
    flight = get_object_or_404(Flight,pk=flight_id)#this tries to find if there is a flight with the given id
    if request.method == 'POST':
        form = AddFlightForm(request.POST, request.FILES, instance=flight)
        if form.is_valid():
            flight.save()
        return redirect('index')
    form = AddFlightForm(instance=flight)
    context = {'form':form, 'flight_id':flight_id}
    return render(request,'edit_flight.html',context)

def delete_flight(request,flight_id):
    flight = get_object_or_404(Flight,pk=flight_id)
    flight.delete()
    return redirect('index')