import csv
from django.core.management.base import BaseCommand
from evaluate_m2.models import EvaluatorMetadata
from evaluate_m2.serializers import EvaluatorMetadataSerializer

class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py import_evaluator_metadata -f [file_path]
    """
    help =  "Imports the evaluator metadata in the given CSV " + \
            "and saves it in the EvaluatorMetadata table in the database. " + \
            "For each row in the CSV, if the 'id' column matches the name of " + \
            "an existing EvaluatorMetadata in the database, that record will " + \
            "be updated with new values from the CSV. Otherwise, a new record " + \
            "will be created."

    default_directory = "evaluate_m2/m2_evaluators/eval_metadata.csv"

    def add_arguments(self, argparser):
        dir_help = "Location of the evaluator metadata file relative to " + \
            f"the `/django` directory. Defaults to {self.default_directory}."

        argparser.add_argument("-f", "--file_path", nargs="?", required=False, help=dir_help)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        if not file_path:
            file_path = self.default_directory

        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            new = 0
            updated = 0
            skipped=0
            rows_count = 0
            for row in reader:
                rows_count += 1
                id = row["id"].strip()
                try:
                    eval = EvaluatorMetadata.objects.get(id=id)
                    from_json = EvaluatorMetadataSerializer(eval, data=row)
                    if from_json.is_valid():
                        from_json.save()
                        updated += 1
                    else:
                        self.stdout.write(f"Error prevented updating {id}: {from_json.errors}")
                        skipped += 1
                except EvaluatorMetadata.DoesNotExist:
                    from_json = EvaluatorMetadataSerializer(data=row)
                    if from_json.is_valid():
                        from_json.save()
                        new += 1
                    else:
                        self.stdout.write(f"Error prevented creating {id}: {from_json.errors}")
                        skipped += 1

        self.stdout.write(f"Read all {rows_count} rows of the CSV.")
        self.stdout.write(f"Created {new} and updated {updated} existing evaluators. Skipped {skipped}.")
        self.stdout.write(f"{EvaluatorMetadata.objects.count()} total evaluators now exist.")
