from django.shortcuts import render
import phonenumbers
from phonenumbers import geocoder, carrier, timezone


# ✅ HOME PAGE
def home(request):
    return render(request, 'home.html')


# ✅ RESULT PAGE
def result(request):

    if request.method == "POST":

        number = request.POST.get('number')

        try:
            parsed_number = phonenumbers.parse(number)

            country = geocoder.description_for_number(parsed_number, "en")

            sim_carrier = carrier.name_for_number(parsed_number, "en")

            timezones = ", ".join(timezone.time_zones_for_number(parsed_number))

            valid = phonenumbers.is_valid_number(parsed_number)

            context = {
                'number': number,
                'country': country if country else "Not Available",
                'carrier': sim_carrier if sim_carrier else "Not Available",
                'timezone': timezones if timezones else "Not Available",
                'valid': valid
            }

        except:
            context = {
                'number': number,
                'country': "Invalid Number",
                'carrier': "Invalid",
                'timezone': "Invalid",
                'valid': False
            }

        return render(request, 'result.html', context)

    return render(request, 'home.html')


# ✅ ABOUT PAGE
def about(request):
    return render(request, 'about.html')