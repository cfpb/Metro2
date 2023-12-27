import csv
from django.core.management.base import BaseCommand
from evaluate_m2.models import EvaluatorMetadata

class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py import_evaluator_metadata -f [file_path]
    """
    help =  "Imports the evaluator metadata in the given CSV " + \
            "and saves it in the EvaluatorMetadata table in the database. " + \
            "If any already exist in the database, they will be deleted and replaced."

    default_directory = "evaluate_m2/m2_evaluators/eval_metadata.csv"

    def add_arguments(self, argparser):
        dir_help = "Location of the evaluator metadata file relative to " + \
            f"the `/django` directory. Defaults to {self.default_directory}."

        argparser.add_argument("-f", "--file_path", nargs="?", required=False, help=dir_help)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        if not file_path:
            file_path = self.default_directory

        EvaluatorMetadata.objects.all().delete()

        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                EvaluatorMetadata.create_from_dict(row)
