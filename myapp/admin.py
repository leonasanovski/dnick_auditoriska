from django.contrib import admin

from myapp.models import Balloon, AirCompanyPilot, Flight, FlightCompany, Pilot, FlightReport, FlightCompanyLog


class AirCompanyPilotInlineAdding(admin.TabularInline):
    model = AirCompanyPilot
    extra = 1
#AirCompanyPilot instances inline when viewing a FlightCompany in the admin panel.

class FlightCompanyAdmin(admin.ModelAdmin):
    list_display = ["company_name", "year_of_establishment", "is_europe_only"]
    inlines = [AirCompanyPilotInlineAdding]
#Associating the inline model in the FlightCompany admin panel view

class FlightAdmin(admin.ModelAdmin):
    exclude = ("user_that_created",)
    # ordering = ['asdad']
    # list_filter = ['asda','asdada1']

    #with this, I exclude this input from the admin panel view
    def save_model(self, request, obj, form, change):
        obj.user_that_created = request.user
        return super(FlightAdmin, self).save_model(request, obj, form, change)
        #here I set automatically the user to be the logged user and I leave the Flight model save to be made by the Flight object
    #with this I am not allowing a flight to be deleted by any user (including the admin)
    #if I want to exclude the admin, then:
    """
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    """

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True  # or False, depending on whether you want to allow list view
        return obj.user_that_created == request.user

    #With this im giving a permission only to the user that created the flight to make changes, not others

admin.site.register(FlightCompany, FlightCompanyAdmin)
#FlightCompanyAdmin defines custom behavior for the admin panel of FlightCompany.
#It allows managing AirCompanyPilot instances directly inside FlightCompany.

admin.site.register(Balloon)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Pilot)
admin.site.register(FlightReport)
admin.site.register(FlightCompanyLog)