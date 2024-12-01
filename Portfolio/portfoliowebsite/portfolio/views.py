from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages  # Import Django's messaging framework
from .models import Project, YouTubeVideo, ContactMessage
from .google_sheets_service import append_to_sheet  # Import your Google Sheets service
from django.utils.translation import gettext as _
import jwt, time
import requests

def portfolio_view(request):
    return render(request, 'portfolio/projects.html')

def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Push data to Google Sheets
        SHEET_ID = '1iwHbX-534gE0Q0is73Kk5-_5njDVi6Iavu3A3BV8dgk'  # Replace with your actual sheet ID
        CONTACT = [[name,email,message]]
        append_to_sheet(SHEET_ID,CONTACT)

        # Add a success message
        success_message = _('Your message has been sent successfully!')
        messages.success(request, success_message)

        return redirect('home')

    projects = Project.objects.all()
    videos = YouTubeVideo.objects.all()
    return render(request, 'portfolio/home.html', {'projects': projects, 'videos': videos})

def dashboard_view(request):
    METABASE_SITE_URL = settings.METABASE_SITE_URL
    METABASE_SECRET_KEY = settings.METABASE_SECRET_KEY

    payload = {
        "resource": {"dashboard": 3},
        "params": {},
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{METABASE_SITE_URL}/embed/dashboard/{token}#&bordered=true&titled=false"
    context = {'iframe_url': iframe_url}
    return render(request, 'portfolio/skillset.html', context)

def streamlit_view(request):
    return render(request, 'portfolio/streamlit.html')

