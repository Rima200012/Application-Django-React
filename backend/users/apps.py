
from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist

class UsersConfig(AppConfig):
     name = 'users'

#     def ready(self):
#         self.create_user_groups()

#     def create_user_groups(self):
#         from django.contrib.auth.models import Group, Permission
#         # Define groups and their permissions
#         groups_permissions = {
#             'recruiter': [
#                 'add_jobpost', 'change_jobpost', 'delete_jobpost', 'view_jobpost',
#                 'view_candidate', 'track_application'
#             ],
#             'candidate': [
#                 'add_job_application', 'change_job_application', 'delete_job_application',
#                 'view_jobpost', 'view_company', 'track_application'
#             ]
#         }
        
#         for group_name, permissions in groups_permissions.items():
#             group, created = Group.objects.get_or_create(name=group_name)
#             if created:
#                 for codename in permissions:
#                     try:
#                         perm = Permission.objects.get(codename=codename)
#                         group.permissions.add(perm)
#                     except Permission.DoesNotExist:
#                         print(f"Permission not found: {codename}")
#                         # Optionally create the permission here if it should exist

#             self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created/updated with permissions.'))


