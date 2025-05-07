"""
A signal is essentially a message sent by one part of the application (the sender) to another part (the receiver) to notify it of some event that has occurred.
These signals will be covered:
- pre_save
- post_save
- pre_delete
- post_delete
"""
from datetime import datetime

from PIL.TiffImagePlugin import DATE_TIME
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from myapp.models import Pilot, Flight, FlightReport, AirCompanyPilot, FlightCompany, FlightCompanyLog

#Defining pre_save
"""
This will be activated before saving something in the DataBase
The sender of the signal will be Pilot

instance - The actual object being saved. You can access or change its fields before it hits the DB.
sender - the model class that sends the signal
**kwargs - extra options (example: using)
"""

#In the pre_save I will make updating the rank function before it goes to data Base
@receiver(pre_save, sender=Pilot)
def update_rank_to_pilot_before_saving(sender, instance, **kwargs):
    print("update_rank_to_pilot_before_saving TRIGGERED")
    if instance.total_hours_on_flight > 1000:
        instance.rank_in_company = 'E' #sets the rank to Expert
    elif instance.total_hours_on_flight > 250:
        instance.rank_in_company = 'I' #sets the rank to Intermediate
    else:
        instance.rank_in_company = 'B' #sets the rank to Beginner

#This is post_save, and will be activated after something is saved in the database
#I have one more parameter called created - It tells you whether this save resulted in a new object being created, or just an update to an existing one(true or false)
#This function is creating a flight report if a new flight is being created
@receiver(post_save, sender=Flight)
def generate_report_for_new_flight(sender, instance,created, **kwargs):

    print("generate_report_for_new_flight TRIGGERED")
    if created:
        print(f"New flight created with code {instance.code}")
        describing_the_flight = f'FLIGHT_CODE: {instance.code}:\nThe flight will departure from '\
                                f'the airport {instance.departure_airport} and land on {instance.landing_airport}.\n'\
                                f'The company that hosts the flight is {instance.flight_company}, with {instance.balloon.balloon_type} balloon.\n' \
                                f'Pilot is Mr./Mrs. {instance.pilot.name} {instance.pilot.surname}\n'
        FlightReport.objects.create(flight_instance=instance,description=describing_the_flight)


#This is pre_delete signal, that is triggered before something is deleted from the database.
#It will make something (the logic in the signal), before we delete an instance

@receiver(pre_delete, sender=FlightCompany)
def move_pilots_to_another_company(sender,instance,**kwargs):
    print("move_pilots_to_another_company TRIGGERED")
    #first we need all the pilots from the FlightCompany
    #we have them in the m-to-n table (AirCompanyPilot model)
    company_pilots_objects = AirCompanyPilot.objects.filter(company=instance).all()
    for airline_pilot in company_pilots_objects:
        new_possible_companies = FlightCompany.objects.exclude(id=instance.id).all()
        #We check if the pilot already exists to the company, so we don't get the exception
        for new_company in new_possible_companies:
            check_if_pilot_already_exists = AirCompanyPilot.objects.filter(company=new_company, pilot=airline_pilot.pilot).exists()
            if not check_if_pilot_already_exists:
                airline_pilot.company = new_company
                airline_pilot.save()
                break
        else:
            print("No new company for the pilot. He already exists to all of them!")

@receiver(post_delete, sender=FlightCompany)
def flight_company_deleting_log(sender, instance, **kwargs):
    total_flights = Flight.objects.filter(flight_company=instance).count()
    year_of_delete = datetime.now().year
    FlightCompanyLog.objects.create(
        name_of_company=instance.company_name,
        total_flights=total_flights,
        description=f'The company {instance.company_name} has been deleted in {year_of_delete} year.\n'
                    f'It had total of {total_flights} flights.\n'
    )