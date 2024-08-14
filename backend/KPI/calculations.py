from pymongo import MongoClient
from django.conf import settings

from Jobs.connectiondb import get_job_application_collection, get_job_post_collection


client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# KPI Calculation Functions
def count_active_job_posts(request):
    job_posts = get_job_post_collection()
    active_posts = job_posts.count_documents({"is_active": "True"})
    return active_posts

def count_total_applications(request):
    applications = get_job_application_collection()
    total_applications = applications.count_documents({})
    return total_applications

def application_conversion_rate(request):
    applications = get_job_application_collection()
    total_applications = applications.count_documents({})
    progressed_applications = applications.count_documents({"status": "progressed"})
    conversion_rate = (progressed_applications / total_applications) * 100 if total_applications else 0
    return conversion_rate

def applications_per_job_post(request):
    applications = get_job_application_collection()
    pipeline = [
        # Group by 'job_post_id' instead of 'jobpostId'
        {"$group": {
            "_id": "$job_post_id",
            "count": {"$sum": 1}
        }},
        # Correcting the lookup to match 'job_post_id' with '_id' of jobposts
        {"$lookup": {
            "from": "jobposts",
            "localField": "_id",
            "foreignField": "_id",  # This assumes job posts are stored by '_id' in 'jobposts'
            "as": "jobpost_details"
        }},
        # Projecting the required fields; getting job title correctly
        {"$project": {
            "job_title": {"$arrayElemAt": ["$jobpost_details.title", 0]},  # Assuming 'title' is the field name in jobposts
            "applications_count": "$count"
        }}
    ]
    result = list(applications.aggregate(pipeline))
    return result


def get_job_application_counts():
    applications = get_job_application_collection()
    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "status": "$_id",
                "count": 1,
                "_id": 0
            }
        }
    ]
    result = list(applications.aggregate(pipeline))
    return result


def get_application_count_by_user(user_id):
    applications = get_job_application_collection()
    pipeline = [
        {"$match": {"added_by": user_id}},  # Filter documents where 'added_by' matches the user_id
        {"$group": {
            "_id": "$added_by",
            "total_applications": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "user_id": "$_id",
            "total_applications": 1
        }}
    ]
    result = list(applications.aggregate(pipeline))
    if result:
        return result[0]
    else:
        return {"user_id": user_id, "total_applications": 0}  # Return zero if no applications found


def get_acceptance_rate():
    applications = get_job_application_collection()
    total_applications = applications.count_documents({})
    accepted_applications = applications.count_documents({"status": "Accepted"})

    if total_applications > 0:
        acceptance_rate = (accepted_applications / total_applications) * 100
    else:
        acceptance_rate = 0

    return acceptance_rate
