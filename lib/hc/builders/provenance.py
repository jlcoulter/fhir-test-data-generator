from math import ceil

from ..base import BaseResourceGenerator


HEALTH_CONNECT_PROVENANCE_PROFILE = "http://digitalhealth.gov.au/fhir/hcpd/StructureDefinition/hcpd-provenance"


class HealthConnectProvenanceGenerator(BaseResourceGenerator):
    resource_type = "Provenance"
    scenario_file = "Provenance.data.csv"

    def build_from_row(self, row):
        ctx = self.context
        provenance = {
            "resourceType": "Provenance",
            "id": ctx.csv_value(row, "resource.id"),
            "meta": ctx.build_meta(HEALTH_CONNECT_PROVENANCE_PROFILE),
            "target": [
                {
                    "extension": [{"url": "http://hl7.org/fhir/StructureDefinition/targetPath", "valueString": ctx.csv_value(row, "target.path")}],
                    "reference": ctx.absolute_reference(ctx.csv_value(row, "target.reference"), "Practitioner"),
                }
            ],
            "recorded": ctx.csv_value(row, "recorded"),
            "activity": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation", "code": ctx.csv_value(row, "activity.code")}]},
            "agent": [
                {
                    "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type", "code": ctx.csv_value(row, "agent.type.code")}]},
                    "role": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/contractsignertypecodes", "code": ctx.csv_value(row, "agent.role.code")}] }],
                    "who": {"reference": ctx.absolute_reference(ctx.csv_value(row, "agent.who.reference"), "Organization")},
                }
            ],
            "entity": [
                {
                    "role": ctx.csv_value(row, "entity0.role"),
                    "what": {"reference": ctx.absolute_reference(ctx.csv_value(row, "entity0.what.reference"), "Practitioner")},
                }
            ],
        }
        return ctx.clean(provenance)

    def build_bulk(self, index):
        ctx = self.context
        practitioner_pool = max(1, ceil(self.args.count / 2))
        organization_pool = max(1, ceil(practitioner_pool / 10))
        practitioner_index = ((index - 1) % practitioner_pool) + 1
        organization_index = ((index - 1) % organization_pool) + 1
        target_path = ctx.random.choice(["name[0].family", "telecom.where(system='phone').value"])
        provenance = {
            "resourceType": "Provenance",
            "id": ctx.bulk_resource_id("provenance", index),
            "meta": ctx.build_meta(HEALTH_CONNECT_PROVENANCE_PROFILE),
            "target": [{"extension": [{"url": "http://hl7.org/fhir/StructureDefinition/targetPath", "valueString": target_path}], "reference": ctx.practitioner_reference(practitioner_index)}],
            "recorded": ctx.faker.iso8601(),
            "activity": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation", "code": "UPDATE"}]},
            "agent": [{"type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type", "code": "author"}]}, "role": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/contractsignertypecodes", "code": "AMENDER"}]}], "who": {"reference": ctx.organization_reference(organization_index)}}],
            "entity": [{"role": "source", "what": {"reference": ctx.practitioner_reference(practitioner_index)}}],
        }
        return ctx.clean(provenance)
