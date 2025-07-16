from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


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

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

@csrf_exempt
def add_review(request):
    print(f"DEBUG: add_review called, user: {request.user}, is_anonymous: {request.user.is_anonymous}")
    
    if(request.user.is_anonymous == False):
        try:
            data = json.loads(request.body)
            print(f"DEBUG: Review data received: {data}")
            
            response = post_review(data)
            print(f"DEBUG: post_review response: {response}")
            
            return JsonResponse({"status":200, "message": "Review posted successfully"})
        except Exception as e:
            print(f"DEBUG: Error in posting review: {e}")
            return JsonResponse({"status":401,"message":f"Error in posting review: {str(e)}"})
    else:
        print("DEBUG: User is not authenticated")
        return JsonResponse({"status":403,"message":"Unauthorized"})
