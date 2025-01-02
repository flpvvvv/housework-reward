import yaml
from django.core.management.base import BaseCommand
from housework.models import Contributor, HouseworkRecord

class Command(BaseCommand):
    help = "Load example data from a YAML file"

    def handle(self, *args, **kwargs):
        with open("data/example_records.yaml", "r") as file:
            data = yaml.safe_load(file)
        
        # Create contributors
        for contributor in data["contributors"]:
            Contributor.objects.get_or_create(id=contributor["id"], name=contributor["name"])

        # Create records
        for record in data["records"]:
            HouseworkRecord.objects.get_or_create(
                id=record["id"],
                record_time=record["record_time"],
                contributor_id=record["contributor_id"],
                points=record["points"],
                note=record["note"],
                image=record["image"],
            )

        self.stdout.write(self.style.SUCCESS("Successfully imported data"))
