from ..base import BaseResourceGenerator


AU_CORE_CONDITION_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-condition"


class AUCoreConditionGenerator(BaseResourceGenerator):
    resource_type = "Condition"
    csv_file = "Condition.csv"

    def build_from_row(self, row):
        ctx = self.context
        condition = {
            "resourceType": "Condition",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_CONDITION_PROFILE),
            "clinicalStatus": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "clinicalStatus_system"), ctx.csv_value(row, "clinicalStatus_code"), ctx.csv_value(row, "clinicalStatus_display"))], ctx.csv_value(row, "clinicalStatus_text")),
            "verificationStatus": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "verificationStatus_system"), ctx.csv_value(row, "verificationStatus_code"), ctx.csv_value(row, "verificationStatus_display"))], None),
            "category": self.build_categories(row),
            "severity": ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "severity_system"), ctx.csv_value(row, "severity_code"), ctx.csv_value(row, "severity_display"))]),
            "code": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "code", 2), ctx.csv_value(row, "code_text")),
            "bodySite": [ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "bodySite_system"), ctx.csv_value(row, "bodySite_code"), ctx.csv_value(row, "bodySite_display"))])],
            "subject": ctx.build_reference(resource_type=ctx.csv_value(row, "subject_reference_type"), reference_id=ctx.csv_value(row, "subject_reference_id"), display=ctx.csv_value(row, "subject_display")),
            "encounter": ctx.build_reference(resource_type=ctx.csv_value(row, "encounter_reference_type"), reference_id=ctx.csv_value(row, "encounter_reference_id")),
            "onsetDateTime": ctx.csv_value(row, "onsetDateTime"),
            "onsetAge": ctx.build_age_from_prefix(row, "onsetAge"),
            "abatementDateTime": ctx.csv_value(row, "abatementDateTime"),
            "recordedDate": ctx.csv_value(row, "recordedDate"),
            "recorder": ctx.build_reference(resource_type=ctx.csv_value(row, "recorder_reference_type"), reference_id=ctx.csv_value(row, "recorder_reference_id")),
            "asserter": ctx.build_reference(resource_type=ctx.csv_value(row, "asserter_reference_type"), reference_id=ctx.csv_value(row, "asserter_reference_id")),
            "evidence": [self.build_evidence(row)],
            "note": [{"text": ctx.csv_value(row, "note_text")}],
        }
        return ctx.clean(condition)

    def build_bulk(self, index):
        ctx = self.context
        patient_index = index
        condition = {
            "resourceType": "Condition",
            "id": ctx.bulk_resource_id("condition", index),
            "meta": ctx.build_meta(AU_CORE_CONDITION_PROFILE),
            "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active", "display": "Active"}]},
            "verificationStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed", "display": "Confirmed"}]},
            "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "problem-list-item"}]}],
            "code": {"coding": [{"system": "http://snomed.info/sct", "code": ctx.random.choice(["38341003", "44054006", "73211009"])}]},
            "subject": {"reference": f"Patient/{ctx.bulk_resource_id('patient', patient_index)}"},
            "recordedDate": ctx.faker.date_this_decade().isoformat(),
        }
        return ctx.clean(condition)

    def build_categories(self, row):
        ctx = self.context
        categories = []
        for index in (1, 2):
            coding = ctx.build_coding(
                ctx.csv_value(row, f"category{index}_system"),
                ctx.csv_value(row, f"category{index}_code"),
                ctx.csv_value(row, f"category{index}_display"),
            )
            category = ctx.build_codeable_concept([coding] if coding else None, ctx.csv_value(row, "category_text") if index == 1 else None)
            if category:
                categories.append(category)
        return categories

    def build_evidence(self, row):
        ctx = self.context
        details = []
        for index in (1, 2, 3):
            reference = ctx.build_reference(reference=ctx.csv_value(row, f"evidence_detail{index}_reference"), display=ctx.csv_value(row, f"evidence_detail{index}_display"))
            if reference:
                details.append(reference)
        return ctx.clean(
            {
                "code": [ctx.build_codeable_concept([ctx.build_coding(ctx.csv_value(row, "evidence_code_system"), ctx.csv_value(row, "evidence_code_code"), ctx.csv_value(row, "evidence_code_display"))])],
                "detail": details,
            }
        )
