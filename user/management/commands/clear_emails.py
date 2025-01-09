from django.core.management.base import BaseCommand
from ...models import User


class Command(BaseCommand):
    help = "Clear emails for inactive users to ensure no remnants block re-signups"

    def handle(self, *args, **kwargs):
        users_to_clear = User.objects.filter(is_active=False).exclude(email="")
        count = users_to_clear.count()

        # Clear emails for those users
        users_to_clear.update(email=None)

        self.stdout.write(self.style.SUCCESS(f"Successfully cleared emails for {count} users"))
