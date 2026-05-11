from ..base import BaseResourceGenerator


AU_CORE_IMMUNIZATION_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-immunization"


class AUCoreImmunizationGenerator(BaseResourceGenerator):
    resource_type = "Immunization"
    csv_file = "Immunization.csv"

    def build_from_row(self, row):
        ctx = self.context
        immunization = {
            "resourceType": "Immunization",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_IMMUNIZATION_PROFILE),
            "identifier": [ctx.build_identifier(system=ctx.csv_value(row, "identifier1_system"), value=ctx.csv_value(row, "identifier1_value"))],
            "status": ctx.csv_value(row, "status"),
            "statusReason": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "statusReason_system"), ctx.csv_value(row, "statusReason_code"), ctx.csv_value(row, "statusReason_display"))]),
            "vaccineCode": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "vaccineCode", 2), ctx.csv_value(row, "vaccineCode_text")),
            "patient": self.build_patient(row),
            "encounter": ctx.build_reference(resource_type=ctx.csv_value(row, "encounter_reference_type"), reference_id=ctx.csv_value(row, "encounter_reference_id")),
            "occurrenceDateTime": ctx.csv_value(row, "occurrenceDateTime"),
            "recorded": ctx.csv_value(row, "recorded"),
            "primarySource": ctx.bool_value(ctx.csv_value(row, "primarySource")) if ctx.csv_value(row, "primarySource") else None,
            "location": ctx.build_reference(resource_type=ctx.csv_value(row, "location_reference_type"), reference_id=ctx.csv_value(row, "location_reference_id")),
            "manufacturer": {"display": ctx.csv_value(row, "manufacturer_display")} if ctx.csv_value(row, "manufacturer_display") else None,
            "lotNumber": ctx.csv_value(row, "lotNumber") or ctx.csv_value(row, "vaccineSerialNumber"),
            "site": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "site_system"), ctx.csv_value(row, "site_code"), ctx.csv_value(row, "site_display"))], ctx.csv_value(row, "site_text")),
            "route": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "route_system"), ctx.csv_value(row, "route_code"), ctx.csv_value(row, "route_display"))], ctx.csv_value(row, "route_text")),
            "performer": [self.build_performer(row)],
            "protocolApplied": [self.build_protocol(row)],
            "note": [{"text": ctx.csv_value(row, "note_text")}],
        }
        return ctx.clean(immunization)

    def build_bulk(self, index):
        ctx = self.context
        immunization = {
            "resourceType": "Immunization",
            "id": ctx.bulk_resource_id("immunization", index),
            "meta": ctx.build_meta(AU_CORE_IMMUNIZATION_PROFILE),
            "status": "completed",
            "vaccineCode": {"coding": [{"system": "http://snomed.info/sct", "code": "1525011000168107", "display": "Comirnaty"}]},
            "patient": {"reference": f"Patient/{ctx.bulk_resource_id('patient', index)}"},
            "occurrenceDateTime": ctx.faker.date_this_decade().isoformat(),
            "primarySource": True,
        }
        return ctx.clean(immunization)

    def build_patient(self, row):
        ctx = self.context
        identifier = ctx.build_reference_identifier(row, "patient_identifier")
        return ctx.build_reference(
            resource_type=ctx.csv_value(row, "patient_reference_type"),
            reference_id=ctx.csv_value(row, "patient_reference_id"),
            display=ctx.csv_value(row, "patient_display"),
            identifier=identifier,
        )

    def build_performer(self, row):
        ctx = self.context
        function = ctx.build_codeable_concept(
            [ctx.build_coding(ctx.csv_value(row, "performer1_function_system"), ctx.csv_value(row, "performer1_function_code"), ctx.csv_value(row, "performer1_function_display"))],
            ctx.csv_value(row, "performer1_function_text"),
        )
        identifier = ctx.build_reference_identifier(row, "performer1_actor_identifier")
        actor = ctx.build_reference(
            resource_type=ctx.csv_value(row, "performer1_actor_reference_type"),
            reference_id=ctx.csv_value(row, "performer1_actor_reference_id"),
            identifier=identifier,
        )
        return ctx.clean({"function": function, "actor": actor})

    def build_protocol(self, row):
        ctx = self.context
        target_disease = ctx.build_codeable_concept(
            [ctx.build_coding(ctx.csv_value(row, "protocolApplied1_targetDisease1_system"), ctx.csv_value(row, "protocolApplied1_targetDisease1_code"), ctx.csv_value(row, "protocolApplied1_targetDisease1_display"))],
            ctx.csv_value(row, "protocolApplied1_targetDisease1_text"),
        )
        return ctx.clean(
            {
                "series": ctx.csv_value(row, "protocolApplied1_series"),
                "targetDisease": [target_disease],
                "doseNumberPositiveInt": ctx._coerce_number(ctx.csv_value(row, "protocolApplied1_doseNumberPositiveInt")),
            }
        )
