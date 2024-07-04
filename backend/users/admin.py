from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Creates read/write groups for recruiters and candidates'

    def handle(self, *args, **kwargs):
        # Creating recruiter group
        recruiter_group, _ = Group.objects.get_or_create(name='Recruiter')
        # You can also add specific permissions to this group
        recruiter_perms = ['add_jobpost', 'change_jobpost', 'delete_jobpost', 'view_jobpost']  # example permissions
        for perm in recruiter_perms:
            permission = Permission.objects.get(codename=perm)
            recruiter_group.permissions.add(permission)

        # Creating candidate group
        candidate_group, _ = Group.objects.get_or_create(name='Candidate')
        # Permissions for candidate
        candidate_perms = ['apply_jobpost', 'view_jobpost']  # example permissions
        for perm in candidate_perms:
            permission = Permission.objects.get(codename=perm)
            candidate_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions.'))

# Register your models here.
