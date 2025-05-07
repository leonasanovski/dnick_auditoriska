from django.shortcuts import render

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

