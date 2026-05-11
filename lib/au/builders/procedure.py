from ..base import BaseResourceGenerator


AU_CORE_PROCEDURE_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-procedure"


class AUCoreProcedureGenerator(BaseResourceGenerator):
    resource_type = "Procedure"
    csv_file = "Procedure.csv"

    def build_from_row(self, row):
        ctx = self.context
        procedure = {
            "resourceType": "Procedure",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_PROCEDURE_PROFILE),
            "status": ctx.csv_value(row, "status"),
            "category": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "category", 1)),
            "code": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "code", 1), ctx.csv_value(row, "code_text")),
            "subject": ctx.build_reference(resource_type=ctx.csv_value(row, "subject_reference_type"), reference_id=ctx.csv_value(row, "subject_reference_id"), display=ctx.csv_value(row, "subject_display")),
            "encounter": ctx.build_reference(resource_type=ctx.csv_value(row, "encounter_reference_type"), reference_id=ctx.csv_value(row, "encounter_reference_id"), display=ctx.csv_value(row, "encounter_display")),
            "performedDateTime": ctx.csv_value(row, "performedDateTime"),
            "performedPeriod": ctx.build_period_from_prefix(row, "performedPeriod"),
            "recorder": ctx.build_reference(resource_type=ctx.csv_value(row, "recorder_reference_type"), reference_id=ctx.csv_value(row, "recorder_reference_id")),
            "asserter": ctx.build_reference(resource_type=ctx.csv_value(row, "asserter_reference_type"), reference_id=ctx.csv_value(row, "asserter_reference_id")),
            "performer": [self.build_performer(row)],
            "location": ctx.build_reference(resource_type="Location", reference_id=ctx.csv_value(row, "location_reference_id")),
            "reasonCode": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "reasonCode1", 1), ctx.csv_value(row, "reasonCode1_text"))],
            "reasonReference": [ctx.build_reference(resource_type=ctx.csv_value(row, "reasonReference1_reference_type"), reference_id=ctx.csv_value(row, "reasonReference1_reference_id"), display=ctx.csv_value(row, "reasonReference1_display"))],
            "bodySite": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "bodySite1", 1), ctx.csv_value(row, "bodySite1_text"))],
            "outcome": {"text": ctx.csv_value(row, "outcome_text")} if ctx.csv_value(row, "outcome_text") else None,
            "focalDevice": [self.build_focal_device(row)],
            "followUp": [{"text": ctx.csv_value(row, "followUp_text")}],
            "note": [{"text": ctx.csv_value(row, "note_text")}],
        }
        return ctx.clean(procedure)

    def build_bulk(self, index):
        ctx = self.context
        procedure = {
            "resourceType": "Procedure",
            "id": ctx.bulk_resource_id("procedure", index),
            "meta": ctx.build_meta(AU_CORE_PROCEDURE_PROFILE),
            "status": "completed",
            "code": {"coding": [{"system": "http://snomed.info/sct", "code": ctx.random.choice(["302497006", "230842002", "36969009"])}]},
            "subject": {"reference": f"Patient/{ctx.bulk_resource_id('patient', index)}"},
            "performedDateTime": ctx.faker.date_this_decade().isoformat(),
        }
        return ctx.clean(procedure)

    def build_performer(self, row):
        ctx = self.context
        return ctx.clean(
            {
                "actor": ctx.build_reference(
                    resource_type=ctx.csv_value(row, "performer1_actor_reference_type"),
                    reference_id=ctx.csv_value(row, "performer1_actor_reference_id"),
                    display=ctx.csv_value(row, "performer1_actor_display"),
                )
            }
        )

    def build_focal_device(self, row):
        ctx = self.context
        return ctx.clean(
            {
                "action": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "focalDevice1_action", 1)),
                "manipulated": {"display": ctx.csv_value(row, "focalDevice1_manipulated_display")} if ctx.csv_value(row, "focalDevice1_manipulated_display") else None,
            }
        )
