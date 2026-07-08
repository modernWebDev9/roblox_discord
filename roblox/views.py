from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings

def google_verify(request):
    file_path = os.path.join(settings.BASE_DIR, 'googleXXXX.html')
    try:
        return render(request, 'people/google1f2e1aafad15e450.html')
    except FileNotFoundError:
        return HttpResponse("Verification file not found.", status=404)