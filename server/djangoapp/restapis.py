# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    # Simple implementation - hardcode the backend URL for testing
    request_url = "http://localhost:3030" + endpoint

    print(f"DEBUG: Attempting to GET {request_url}")

    try:
        import requests
        response = requests.get(request_url, timeout=10)
        print(f"DEBUG: Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            # Check if data is list and get length or say 'non-list'
            items_info = len(data) if isinstance(data, list) else 'non-list'
            print(f"DEBUG: Got {items_info} items")
            return data
        else:
            print(f"DEBUG: HTTP Error {response.status_code}")
            return None

    except Exception as e:
        print(f"DEBUG: Exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments


def post_review(data_dict):
    request_url = "http://localhost:3030/insert_review"
    print(f"DEBUG: Posting review to {request_url}")
    print(f"DEBUG: Review data: {data_dict}")
    try:
        response = requests.post(request_url, json=data_dict, timeout=10)
        print(f"DEBUG: Response status code: {response.status_code}")
        response_data = response.json()
        print(f"DEBUG: Response data: {response_data}")
        return response_data
    except Exception as e:
        print(f"DEBUG: Network exception occurred: {e}")
        raise e
