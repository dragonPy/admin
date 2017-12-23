from django.core.management.base import BaseCommand, CommandError
from settings.models import Country, Bank, ProvinceCN, FundLimit, KYCLevel, PointLevel, Language
import sys, os

DATA_DICT={
    'bank': Bank,
    'country': Country,
    'province_cn': ProvinceCN,
    'fund_limit': FundLimit,
    'kyc_level': KYCLevel,
    'point_level': PointLevel,
    'languages': Language
}

class Command(BaseCommand):
    help = 'clear initial data: [country], [bank], [cn_province], [fund_limit], [languages]'

    def add_arguments(self, parser):
        parser.add_argument('data_type', nargs='+', type=str)

    def handle(self, *args, **options):
        for data_type in options['data_type']:
            DATA_DICT[data_type].objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully removed "%s"' % data_type))