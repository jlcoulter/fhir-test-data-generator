from ..base import BaseResourceGenerator


AU_CORE_ALLERGY_INTOLERANCE_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-allergyintolerance"


class AUCoreAllergyIntoleranceGenerator(BaseResourceGenerator):
    resource_type = "AllergyIntolerance"
    csv_file = "AllergyIntolerance.csv"

    def build_from_row(self, row):
        ctx = self.context
        allergy = {
            "resourceType": "AllergyIntolerance",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_ALLERGY_INTOLERANCE_PROFILE),
            "clinicalStatus": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "clinicalStatus_system"), ctx.csv_value(row, "clinicalStatus_code"), ctx.csv_value(row, "clinicalStatus_display"))], ctx.csv_value(row, "clinicalStatus_text")),
            "verificationStatus": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "verificationStatus_system"), ctx.csv_value(row, "verificationStatus_code"), ctx.csv_value(row, "verificationStatus_display"))], ctx.csv_value(row, "verificationStatus_text")),
            "type": ctx.csv_value(row, "type"),
            "category": [ctx.csv_value(row, "category")] if ctx.csv_value(row, "category") else [],
            "criticality": ctx.csv_value(row, "criticality"),
            "code": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "code", 2), ctx.csv_value(row, "code_text")),
            "patient": self.build_patient(row),
            "encounter": {"display": ctx.csv_value(row, "encounter_display")} if ctx.csv_value(row, "encounter_display") else None,
            "onsetDateTime": ctx.csv_value(row, "onsetDateTime"),
            "onsetAge": ctx.build_age_from_prefix(row, "onsetAge"),
            "recordedDate": ctx.csv_value(row, "recordedDate"),
            "recorder": self.build_actor(row, "recorder"),
            "asserter": self.build_actor(row, "asserter"),
            "reaction": [self.build_reaction(row)],
        }
        return ctx.clean(allergy)

    def build_bulk(self, index):
        ctx = self.context
        allergy = {
            "resourceType": "AllergyIntolerance",
            "id": ctx.bulk_resource_id("allergyintolerance", index),
            "meta": ctx.build_meta(AU_CORE_ALLERGY_INTOLERANCE_PROFILE),
            "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical", "code": "active"}]},
            "verificationStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification", "code": "confirmed"}]},
            "category": [ctx.random.choice(["food", "medication", "environment"])],
            "code": {"coding": [{"system": "http://snomed.info/sct", "code": ctx.random.choice(["102263004", "227493005", "33008008"])}]},
            "patient": {"reference": f"Patient/{ctx.bulk_resource_id('patient', index)}"},
        }
        return ctx.clean(allergy)

    def build_patient(self, row):
        ctx = self.context
        identifier = ctx.build_reference_identifier(row, "patient_identifier")
        return ctx.build_reference(
            resource_type=ctx.csv_value(row, "patient_reference_type"),
            reference_id=ctx.csv_value(row, "patient_reference_id"),
            identifier=identifier,
        )

    def build_actor(self, row, prefix):
        ctx = self.context
        identifier = ctx.build_reference_identifier(row, f"{prefix}_identifier")
        return ctx.build_reference(
            resource_type=ctx.csv_value(row, f"{prefix}_reference_type"),
            reference_id=ctx.csv_value(row, f"{prefix}_reference_id"),
            identifier=identifier,
        )

    def build_reaction(self, row):
        ctx = self.context
        manifestation = []
        for index in (1, 2, 3):
            value = ctx.build_codeable_concept(
                [ctx.build_coding(ctx.csv_value(row, f"reaction_manifestation{index}_system"), ctx.csv_value(row, f"reaction_manifestation{index}_code"), ctx.csv_value(row, f"reaction_manifestation{index}_display"))],
                ctx.csv_value(row, f"reaction_manifestation{index}_text"),
            )
            if value:
                manifestation.append(value)
        return ctx.clean(
            {
                "substance": ctx.build_codeable_concept(
                    [ctx.build_coding(ctx.csv_value(row, "reaction_substance_system"), ctx.csv_value(row, "reaction_substance_code"), ctx.csv_value(row, "reaction_substance_display"))],
                    ctx.csv_value(row, "reaction_substance_text"),
                ),
                "manifestation": manifestation,
                "severity": ctx.csv_value(row, "reaction_severity"),
            }
        )
