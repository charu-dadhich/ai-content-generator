import os
import json
import traceback
from django.core.management.base import BaseCommand
from django.db import transaction
from app.base.models import Standard, Board, Subject, Chapter, ServiceType, BloomsLevel
from app.question.models import CustomQuestionTypeDetail


class Command(BaseCommand):
    help = "Seed the data into base models - Standard, subjects, Boards"

    def handle(self, *args, **options):
        current_path = os.path.abspath(__file__)
        seed_file_path = {
            # Board: '../../../../../seeders/boards.json',
            # Subject: '../../../../../seeders/subjects.json',
            # Standard: '../../../../../seeders/classes.json',
            # Chapter: '../../../../../seeders/seed_10.json',
            ServiceType: '../../../../../seeders/question_type.json'
            # CustomQuestionTypeDetail: '../../../../../seeders/detail_question_type.json',
            # BloomsLevel: '../../../../../seeders/bloom_levels.json'
        }
        for key, val in seed_file_path.items():
            file_path = os.path.abspath(os.path.join(current_path, val))
            model_name = key
            json_file_name = os.path.basename(val)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)

                # if not isinstance(raw_data, list):
                #     self.stdout.write(self.style.ERROR(f"Error: JSON file '{json_file_name}' does not contain a list of objects. Skipping {model_name}."))
                #     continue

                instances_to_create = []
                for item_dict in raw_data:
                    # if not isinstance(item_dict, dict):
                    #     self.stdout.write(self.style.WARNING(f"Warning: Item in {json_file_name} is not a dictionary: {item_dict}. Skipping."))
                    #     continue

                    try:
                        instance = model_name(**item_dict)
                        instances_to_create.append(instance)
                    except TypeError as te:
                        self.stdout.write(self.style.ERROR(f"Error creating {model_name} instance from {item_dict}: {te}. Check JSON keys vs model fields."))
                        continue

                if not instances_to_create:
                    self.stdout.write(self.style.NOTICE(f"No valid {model_name} instances prepared from {json_file_name}. Skipping bulk_create."))
                    continue

                with transaction.atomic():
                    created_count = model_name.objects.bulk_create(
                        instances_to_create,
                        ignore_conflicts=True
                    )

                if created_count:
                    self.stdout.write(self.style.SUCCESS(f"Successfully inserted {len(created_count)} new {model_name} objects."))
                else:
                    self.stdout.write(self.style.NOTICE(f"No new {model_name} objects were inserted (all may already exist)."))

            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR(f"Error: Could not decode JSON from {json_file_name}. Check file format."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An unexpected error occurred while processing {json_file_name}: {e}"))
                self.stdout.write(traceback.format_exc())

        self.stdout.write(self.style.SUCCESS("\nDatabase seeding complete."))
