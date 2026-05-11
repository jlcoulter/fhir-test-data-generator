from ..base import BaseResourceGenerator


AU_CORE_MEDICATION_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-medication"


class AUCoreMedicationGenerator(BaseResourceGenerator):
    resource_type = "Medication"
    csv_file = "Medication.csv"

    def build_from_row(self, row):
        ctx = self.context
        medication = {
            "resourceType": "Medication",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_MEDICATION_PROFILE),
            "code": ctx.build_codeable_concept(self.build_medication_codings(row), ctx.csv_value(row, "code_text")),
            "form": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "form", 3), ctx.csv_value(row, "form_text")),
            "ingredient": [self.build_ingredient(row)],
        }
        return ctx.clean(medication)

    def build_bulk(self, index):
        ctx = self.context
        medication = {
            "resourceType": "Medication",
            "id": ctx.bulk_resource_id("medication", index),
            "meta": ctx.build_meta(AU_CORE_MEDICATION_PROFILE),
            "code": {"coding": [{"system": "http://snomed.info/sct", "code": ctx.random.choice(["320000009", "926214011000036103"])}]},
            "form": {"coding": [{"system": "http://snomed.info/sct", "code": "385055001", "display": "Tablet dose form"}]},
        }
        return ctx.clean(medication)

    def build_medication_codings(self, row):
        ctx = self.context
        codings = []
        medication_type_code = ctx.csv_value(row, "code_coding1_medicationType_code")
        medication_type_display = ctx.csv_value(row, "code_coding1_medicationType_display")
        if medication_type_code or medication_type_display:
            codings.append(
                ctx.build_coding(
                    "http://terminology.hl7.org.au/CodeSystem/medication-type",
                    medication_type_code,
                    medication_type_display,
                )
            )
        codings.extend(ctx.build_codings_from_prefix(row, "code", 3))
        return [coding for coding in codings if coding]

    def build_ingredient(self, row):
        ctx = self.context
        return ctx.clean(
            {
                "itemCodeableConcept": ctx.build_codeable_concept(
                    ctx.build_codings_from_prefix(row, "ingredient_itemCodeableConcept", 2)
                ),
                "strength": {
                    "numerator": ctx.build_quantity_from_prefix(row, "ingredient_strength_numerator"),
                    "denominator": ctx.build_quantity_from_prefix(row, "ingredient_strength_denominator"),
                },
            }
        )
