from django.contrib.auth.models import User

# Delete users with empty usernames
empty_users = User.objects.filter(username='')
count = empty_users.count()
empty_users.delete()
print(f"Deleted {count} users with empty usernames")
