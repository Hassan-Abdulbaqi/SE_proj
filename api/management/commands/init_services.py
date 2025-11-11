from decimal import Decimal

from django.core.management.base import BaseCommand

from api.models import Service


class Command(BaseCommand):
    help = 'Initialize services (Electricity, Water, Gas)'

    def handle(self, *args, **options):
        services = [
            {
                'service_type': 'electricity',
                'name_ar': 'كهرباء',
                'name_en': 'Electricity',
                'price_per_unit': Decimal('200.00'),
                'unit_name': 'kWh',
                'unit_name_ar': 'كيلوواط'
            },
            {
                'service_type': 'water',
                'name_ar': 'ماء',
                'name_en': 'Water',
                'price_per_unit': Decimal('150.00'),
                'unit_name': 'Liter',
                'unit_name_ar': 'لتر'
            },
            {
                'service_type': 'gas',
                'name_ar': 'غاز',
                'name_en': 'Gas',
                'price_per_unit': Decimal('180.00'),
                'unit_name': 'm³',
                'unit_name_ar': 'متر مكعب'
            }
        ]
        
        for service_data in services:
            service, created = Service.objects.get_or_create(
                service_type=service_data['service_type'],
                defaults=service_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created service: {service.name_en}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Service already exists: {service.name_en}')
                )

