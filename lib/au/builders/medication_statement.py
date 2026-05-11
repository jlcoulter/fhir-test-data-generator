from ..base import BaseResourceGenerator


AU_CORE_MEDICATION_STATEMENT_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-medicationstatement"


class AUCoreMedicationStatementGenerator(BaseResourceGenerator):
    resource_type = "MedicationStatement"
    csv_file = "MedicationStatement.csv"

    def build_from_row(self, row):
        ctx = self.context
        medication_statement = {
            "resourceType": "MedicationStatement",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_MEDICATION_STATEMENT_PROFILE),
            "status": ctx.csv_value(row, "status"),
            "contained": [self.build_contained_medication(row)],
            "medicationCodeableConcept": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "medication", 2), ctx.csv_value(row, "medication_text")),
            "medicationReference": ctx.build_reference(resource_type="Medication", reference_id=ctx.csv_value(row, "medication_reference_id"), display=ctx.csv_value(row, "medication_display")),
            "subject": ctx.build_reference(resource_type="Patient", reference_id=ctx.csv_value(row, "subject_reference_id"), display=ctx.csv_value(row, "subject_display")),
            "effectiveDateTime": ctx.csv_value(row, "effectiveDateTime"),
            "effectivePeriod": ctx.build_period_from_prefix(row, "effectivePeriod"),
            "dateAsserted": ctx.csv_value(row, "dateAsserted"),
            "reasonCode": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "reasonCode1", 1), ctx.csv_value(row, "reasonCode1_text"))],
            "reasonReference": [ctx.build_reference(reference=ctx.csv_value(row, "reasonReference1_reference"))],
            "dosage": [self.build_dosage(row)],
        }
        return ctx.clean(medication_statement)

    def build_bulk(self, index):
        ctx = self.context
        medication_statement = {
            "resourceType": "MedicationStatement",
            "id": ctx.bulk_resource_id("medicationstatement", index),
            "meta": ctx.build_meta(AU_CORE_MEDICATION_STATEMENT_PROFILE),
            "status": "active",
            "subject": {"reference": f"Patient/{ctx.bulk_resource_id('patient', index)}"},
            "effectiveDateTime": ctx.faker.date_this_decade().isoformat(),
        }
        return ctx.clean(medication_statement)

    def build_contained_medication(self, row):
        ctx = self.context
        if not any([ctx.csv_value(row, "contained_medication_code_coding1_system"), ctx.csv_value(row, "contained_medication_code_text")]):
            return None
        return ctx.clean(
            {
                "resourceType": "Medication",
                "id": ctx.csv_value(row, "medication_reference_id") or "med1",
                "code": ctx.build_codeable_concept(
                    [
                        ctx.build_coding(
                            ctx.csv_value(row, "contained_medication_code_coding1_system"),
                            ctx.csv_value(row, "contained_code_coding1_code"),
                            ctx.csv_value(row, "contained_medication_code_coding1_display"),
                        )
                    ],
                    ctx.csv_value(row, "contained_medication_code_text"),
                ),
                "form": ctx.build_codeable_concept(
                    [
                        ctx.build_coding(
                            ctx.csv_value(row, "contained_medication_form_coding1_system"),
                            ctx.csv_value(row, "contained_medication_form_coding1_code"),
                            ctx.csv_value(row, "contained_medication_form_coding1_display"),
                        )
                    ],
                    ctx.csv_value(row, "contained_medication_form_text"),
                ),
            }
        )

    def build_dosage(self, row):
        ctx = self.context
        return ctx.clean(
            {
                "text": ctx.csv_value(row, "dosageInstruction_text"),
                "timing": {
                    "repeat": {
                        "frequency": ctx._coerce_number(ctx.csv_value(row, "dosageInstruction_timing_repeat_frequency")),
                        "frequencyMax": ctx._coerce_number(ctx.csv_value(row, "dosageInstruction_timing_repeat_frequencyMax")),
                        "period": ctx._coerce_number(ctx.csv_value(row, "dosageInstruction_timing_repeat_period")),
                        "periodMax": ctx._coerce_number(ctx.csv_value(row, "dosageInstruction_timing_repeat_periodMax")),
                        "periodUnit": ctx.csv_value(row, "dosageInstruction_timing_repeat_periodUnit"),
                    }
                },
                "asNeededBoolean": ctx.bool_value(ctx.csv_value(row, "dosageInstruction_asNeededBoolean")) if ctx.csv_value(row, "dosageInstruction_asNeededBoolean") else None,
                "route": ctx.build_codeable_concept(
                    [
                        ctx.build_coding(
                            ctx.csv_value(row, "dosageInstruction_route_coding_system"),
                            ctx.csv_value(row, "dosageInstruction_route_coding_code"),
                            ctx.csv_value(row, "dosageInstruction_route_coding_display"),
                        )
                    ],
                    ctx.csv_value(row, "dosageInstruction_route_text"),
                ),
                "doseAndRate": [{"doseQuantity": ctx.build_quantity_from_prefix(row, "dosageInstruction_doseAndRate_doseQuantity")}],
            }
        )
