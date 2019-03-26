from django.shortcuts import render
from .models import Emitent, Industry, IndustrySubgroup


# Render information for main page
def main_page(request):
    # Get basic emitent info, ready to publish
    # TODO: Card contains NAME, INDUSTRY, SUB INDUSTRY, and processed CHARTS
    # TODO: Need to add them in query sets, and filter by some criteria
    emitents_card = Emitent.objects.filter(publish_stage__contains='3')
    return render(request, 'emitent/main.html', {'cards': emitents_card})
