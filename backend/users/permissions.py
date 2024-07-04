from functools import wraps
from django.http import JsonResponse
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework.authentication import get_authorization_header


def decode_token(token):
    try:
        # Decode the token. This does not check if the token is expired.
        untyped_token = UntypedToken(token)

        # Get user ID from token. Assumes your token has a 'user_id' claim.
        user_id = untyped_token[api_settings.USER_ID_CLAIM]

        return user_id
    except (InvalidToken, TokenError) as e:
        raise exceptions.AuthenticationFailed('Invalid token or expired token') from e




def allowed_roles(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view, request, *args, **kwargs):
            # Get the authorization header using DRF's built-in method
            auth_header = get_authorization_header(request).split()

            if not auth_header or len(auth_header) != 2 or auth_header[0].lower() != b'bearer':
                return JsonResponse({"message": "No valid token provided"}, status=401)

            try:
                token = auth_header[1]
                decoded_token = UntypedToken(token)
                user_id = decoded_token['user_id']  # Ensure 'user_id' is a claim in the token
                db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
                user = db.users.find_one({"_id": ObjectId(user_id)})

                if user and user.get('role') in roles:
                    # Call the view function with the view instance `view`
                    return view_func(view, request, *args, **kwargs)
                else:
                    return JsonResponse({"message": "You do not have permission to perform this action"}, status=403)
            except (InvalidToken, TokenError) as e:
                return JsonResponse({"message": "Invalid token: " + str(e)}, status=401)
            except Exception as e:
                return JsonResponse({"message": "Error during authentication: " + str(e)}, status=400)

        return wrapper
    return decorator




