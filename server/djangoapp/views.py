from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
def login_user(request):
    if request.method == 'GET':
        # Show login form for GET requests
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        # Handle both form data and JSON data
        if request.content_type == 'application/json':
            # Handle JSON API requests
            try:
                data = json.loads(request.body)
                username = data['userName']
                password = data['password']
            except (json.JSONDecodeError, KeyError):
                return JsonResponse({"error": "Invalid JSON data"}, status=400)
        else:
            # Handle HTML form submissions
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        # Try to authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            
            # Return appropriate response based on request type
            if request.content_type == 'application/json':
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                messages.success(request, f'Welcome back, {username}!')
                return render(request, 'login_success.html', {'username': username})
        else:
            # Authentication failed
            if request.content_type == 'application/json':
                return JsonResponse({"userName": username, "status": "Failed"}, status=401)
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'login.html')
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    
    # Check if user already exists
    try:
        User.objects.get(username=username)
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)
    except User.DoesNotExist:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        # Log in the user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
