import os

from lib.base import ProfileContext
from lib.base import BaseResourceGenerator as _BaseResourceGenerator


class HealthConnectContext(ProfileContext):
    def candidate_input_paths(self, file_name):
        return [
            os.path.join(self.input_dir, file_name),
            os.path.join(self.input_dir, "health-connect-26.0.0", file_name),
        ]

    def normalize_token(self, value):
        text = str(value).strip()
        if text.startswith("#"):
            return text[1:]
        return text

    def token_value(self, row, key):
        return self.normalize_token(self.csv_value(row, key))

    def bool_value(self, value):
        return self.normalize_token(value).lower() == "true"

    def float_value(self, value):
        text = str(value).strip()
        return float(text) if text else None

    def slugify(self, value):
        normalized = self.normalize_text(value).lower().replace(" ", "")
        return normalized or "healthconnect"

    def bulk_resource_id(self, resource_name, index):
        return f"healthconnect-{resource_name}-{index:07d}"

    def make_time_extension(self, time_value, timezone):
        if not time_value:
            return None, None
        primitive_extension = None
        if timezone:
            primitive_extension = {
                "extension": [
                    {
                        "url": "http://hl7.org/fhir/StructureDefinition/timezone",
                        "valueCode": timezone,
                    }
                ]
            }
        return time_value, primitive_extension

    def healthcare_service_reference(self, index):
        return f"HealthcareService/{self.bulk_resource_id('healthcareservice', index)}"

    def endpoint_reference(self, index):
        return f"Endpoint/{self.bulk_resource_id('endpoint', index)}"


class BaseResourceGenerator(_BaseResourceGenerator):
    def __init__(self, args):
        self.args = args
        self.context = HealthConnectContext(args)
