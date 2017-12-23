from django.core.management.base import BaseCommand, CommandError
from users.models import User
from django.contrib.auth.models import User
import sys, os

# current path of the file
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

CSV_DIR = dir_path + '/../../../../data/%s.csv'

class Command(BaseCommand):
    help = 'create super users, [username]'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options['username']:
            user=User.objects.create_user(username, password='useradmin', is_superuser=True, is_staff=True)
            self.stdout.write(self.style.SUCCESS('Successfully Created Superuser "%s"' % username))