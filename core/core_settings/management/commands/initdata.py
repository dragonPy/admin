from django.core.management.base import BaseCommand, CommandError
from core_settings.models import Country, Bank, ProvinceCN, FundLimit, KYCLevel, PointLevel, Language
import sys, os

# current path of the file
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

CSV_DIR = dir_path + '/../../../../data/%s.csv'

class Command(BaseCommand):
    help = 'import initial data: [country], [bank], [province_cn], [fund_limit], [kyc_level], [point_level], [languages]'

    def add_arguments(self, parser):
        parser.add_argument('data_type', nargs='+', type=str)

    def handle(self, *args, **options):
        for data_type in options['data_type']:
            lines = open(CSV_DIR % data_type, 'r').readlines()
            for line in lines:
                items = line.split(",")
                if data_type == 'bank':
                    [code, name_str_cn, card_length_enterprise, card_length_private] = items
                    Bank.objects.create(
                        code=code,
                        name_str_cn=name_str_cn,
                        card_length_enterprise=card_length_enterprise,
                        card_length_private=card_length_private 
                    )
                if data_type == 'country':
                    [name, name_en, iso2, mobile_code] = items
                    Country.objects.create(
                        name=name.replace('"', ''), 
                        name_en=name_en.replace('"', ''), 
                        iso2=iso2.replace('"', ''), 
                        mobile_code=mobile_code.replace('"', '')
                    )
                if data_type == 'province_cn':
                    [district_id,district_name,city_id,city_name,province_id,province_name] = items
                    ProvinceCN.objects.create(
                        district_id=district_id,
                        district_name=district_name,
                        city_id=city_id,
                        city_name=city_name,
                        province_id=province_id,
                        province_name=province_name
                    )
                if data_type == 'fund_limit':
                    [span,currency,withdraw,deposit,memo] = items
                    w = float(withdraw) if withdraw != '' else None
                    d = float(deposit) if deposit != '' else None
                    FundLimit.objects.create(
                        span=span,
                        currency=currency,
                        withdraw=w,
                        deposit=d,
                        memo=memo
                    )

                if data_type == 'kyc_level':
                    [alien,level,condition,limits] = items
                    l = FundLimit.objects.filter(memo=limits) if limits != '' else 0
                    k = KYCLevel.objects.create(
                        alien=alien,
                        level=level,
                        condition=condition,
                    )
                    if l:
                        for limit in l:
                            k.limits.add(limit)

                if data_type == 'languages':               
                    [alpha3b, alpha2, english] = items
                    Language.objects.create(
                        alpha3b=alpha3b.replace('"',''),
                        alpha2=alpha2.replace('"',''),
                        english=english.replace('"','')
                    )

                if data_type == 'point_level':
                    [level, level_str, point_upper, point_lower, withdraw_rate, loan_leverage] = items
                    pl = int(point_upper) if point_upper != '' else None
                    PointLevel.objects.create(
                        level=int(level),
                        level_str=level_str,
                        point_upper=pl,
                        point_lower=int(point_lower),
                        withdraw_rate=float(withdraw_rate),
                        loan_leverage=float(loan_leverage)
                    )

            self.stdout.write(self.style.SUCCESS('Successfully imported "%s"' % data_type))