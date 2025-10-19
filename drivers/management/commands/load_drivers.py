import csv
import os
from django.core.management.base import BaseCommand, CommandError
from drivers.models import Driver


class Command(BaseCommand):
    help = 'Load drivers from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            nargs='?',
            default=None,
            help='Path to the CSV file containing driver data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing drivers before loading'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        # If no file specified, look for the default seed data file
        if not csv_file:
            # Try to find the seed data file
            possible_paths = [
                '../AssignmentStatement/rhfd_seed dataset/rhfd_drivers.csv',
                '../../AssignmentStatement/rhfd_seed dataset/rhfd_drivers.csv',
                '../../../AssignmentStatement/rhfd_seed dataset/rhfd_drivers.csv',
                'rhfd_drivers.csv',
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    csv_file = path
                    break
            
            if not csv_file:
                raise CommandError(
                    'CSV file not found. Please provide the path to the CSV file:\n'
                    'python manage.py load_drivers <path_to_csv>'
                )
        
        if not os.path.exists(csv_file):
            raise CommandError(f'CSV file "{csv_file}" does not exist')

        # Clear existing drivers if requested
        if options['clear']:
            Driver.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Cleared all existing drivers')
            )

        # Load drivers from CSV
        created_count = 0
        updated_count = 0
        error_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        driver_id = int(row['driver_id'])
                        name = row['name']
                        phone = row['phone']
                        vehicle_type = row['vehicle_type']
                        vehicle_plate = row['vehicle_plate']
                        is_active = row['is_active'].lower() in ['true', '1', 'yes']
                        
                        # Try to get existing driver
                        driver, created = Driver.objects.update_or_create(
                            driver_id=driver_id,
                            defaults={
                                'name': name,
                                'phone': phone,
                                'vehicle_type': vehicle_type,
                                'vehicle_plate': vehicle_plate,
                                'is_active': is_active,
                            }
                        )
                        
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error processing row {reader.line_num}: {str(e)}'
                            )
                        )
                        continue
        
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')
        
        # Print summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully loaded drivers from {csv_file}'
            )
        )
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(f'  Errors: {error_count}')
            )

