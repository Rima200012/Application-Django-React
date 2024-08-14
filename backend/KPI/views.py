from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from django.conf import settings
from requests.exceptions import HTTPError

from django.http import JsonResponse
from .calculations import (
    count_active_job_posts, count_total_applications,
    application_conversion_rate, applications_per_job_post,
    get_application_count_by_user, get_acceptance_rate,
)


# Connection and collection access setup
client = MongoClient('mongodb://localhost:27017/')
db = client[settings.MONGO_DB_NAME]

def get_job_posts_collection():
    return db['job_posts']

def get_job_application_collection():
    return db['job_applications']

def get_users_collection():
    return db['users']

def get_files_collection():
    return db['fs.files']

# Example KPI Functions

from django.http import JsonResponse
from django.views import View
from .calculations import (
    count_active_job_posts, count_total_applications,
    application_conversion_rate, applications_per_job_post, get_job_application_counts
)

class ActiveJobPostsView(View):
    def get(self, request, *args, **kwargs):
        # Ensuring the response is correctly wrapped in JsonResponse
        count = count_active_job_posts(request)
        if isinstance(count, int):
            return JsonResponse({'active_job_posts': count})
        else:
            # Handling unexpected response types
            return JsonResponse({'error': 'Invalid response type from KPI calculation'}, status=500)

class TotalApplicationsView(View):
    def get(self, request, *args, **kwargs):
        count = count_total_applications(request)
        if isinstance(count, int):
            return JsonResponse({'total_applications': count})
        else:
            return JsonResponse({'error': 'Invalid response type from KPI calculation'}, status=500)

class ConversionRateView(View):
    def get(self, request, *args, **kwargs):
        rate = application_conversion_rate(request)
        if isinstance(rate, (int, float)):
            return JsonResponse({'conversion_rate': rate})
        else:
            return JsonResponse({'error': 'Invalid response type from KPI calculation'}, status=500)

class ApplicationsPerPostView(View):
    def get(self, request, *args, **kwargs):
        data = applications_per_job_post(request)
        if isinstance(data, list):  # Assuming this returns a list
            return JsonResponse({'applications_per_post': data})
        else:
            return JsonResponse({'error': 'Invalid response type from KPI calculation'}, status=500)
# Function to calculate the average time to fill a job post
class AverageTimeToFillView(View):
    def get(self, request, *args, **kwargs):
        job_posts = get_job_posts_collection()
        pipeline = [
            {"$match": {"status": "filled"}},
            {"$project": {
                "time_to_fill": {"$subtract": ["$dateFilled", "$datePosted"]},
            }},
            {"$group": {
                "_id": None,
                "average_time_to_fill": {"$avg": "$time_to_fill"}
            }}
        ]
        result = list(job_posts.aggregate(pipeline))
        average_days = result[0]['average_time_to_fill'] / (1000 * 60 * 60 * 24) if result else 0
        return JsonResponse({'average_time_to_fill': average_days})
    

class JobApplicationStatusView(View):
    def get(self, request, *args, **kwargs):
        data = get_job_application_counts()
        return JsonResponse(data, safe=False)  # Use safe=False to allow serialization of lists
    

class UserApplicationsView(View):
    def get(self, request, user_id, *args, **kwargs):
        data = get_application_count_by_user(user_id)
        return JsonResponse(data)
    

class AcceptanceRateView(View):
    def get(self, request, *args, **kwargs):
        rate = get_acceptance_rate()
        return JsonResponse({'acceptance_rate': rate})



CLIENT_ID = '7c3bcb52-41c1-4d31-8343-b66b2dc90924'
CLIENT_SECRET = 'kkd8Q~vWCdHfbvkakSRfjbl4ON0LWwEFXUQalbv3'
TENANT_ID = '4a150cd5-c43e-4caf-a5a8-f688d4c69d7a'
WORKSPACE_ID = 'e98612cc-532e-4c8a-aba9-1ec88821529f'

# Separate report and dataset IDs for candidate and recruiter
REPORTS = {
    'candidate': {
        'report_id': '57b3cc41-a9ed-4705-b3ad-7935c5c54479',
        'dataset_id': '612dcf07-b144-4aa3-83b5-545957f27f77',
        'embed_url': 'https://app.powerbi.com/reportEmbed?reportId=57b3cc41-a9ed-4705-b3ad-7935c5c54479&groupId=e98612cc-532e-4c8a-aba9-1ec88821529f'
    },
    'recruiter': {
        'report_id': '6dc55b9c-036d-4544-8aff-77a73d6fbaaf',
        'dataset_id': 'a11e502c-5cb1-4ce8-9476-142061de9054',
        'embed_url': 'https://app.powerbi.com/reportEmbed?reportId=6dc55b9c-036d-4544-8aff-77a73d6fbaaf&groupId=e98612cc-532e-4c8a-aba9-1ec88821529f'

    }
}
def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an error if the request failed
    token_response = response.json()
    print("Token response:", token_response)  # Debugging line
    return token_response.get('access_token')

def get_report_embed_details(workspace_id, report_id, access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    print("Get report details response:", response.text)  # Debugging line
    response.raise_for_status()
    return response.json()

def generate_embed_token(workspace_id, report_id, dataset_id, access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/GenerateToken"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "datasets": [
            {
                "id": dataset_id
            }
        ],
        "reports": [
            {
                "id": report_id
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    print("Generate embed token response:", response.text)  # Debugging line
    response.raise_for_status()
    return response.json()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_embed_config(request, user_type):
    try:
        access_token = get_access_token()
        report_info = REPORTS.get(user_type)
        
        if not report_info:
            return Response({'error': 'Invalid user type'}, status=400)

        report_id = report_info['report_id']
        dataset_id = report_info['dataset_id']
        embed_url = report_info['embed_url']
        
        embed_token = generate_embed_token(WORKSPACE_ID, report_id, dataset_id, access_token)

        embed_config = {
            "type": "report",
            "id": report_id,
            "embedUrl": embed_url,
            "accessToken": embed_token.get('token'),
            "tokenType": "Bearer",
            "settings": {
                "panes": {
                    "filters": {
                        "visible": False
                    },
                    "pageNavigation": {
                        "visible": False
                    }
                }
            }
        }

        return Response(embed_config)
    except requests.exceptions.RequestException as e:
        print("Error in get_embed_config:", e)
        return Response({"error": str(e)}, status=500)
