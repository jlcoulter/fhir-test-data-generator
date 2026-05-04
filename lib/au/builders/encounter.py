from math import ceil

from ..base import BaseResourceGenerator


AU_CORE_ENCOUNTER_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-encounter"


class AUCoreEncounterGenerator(BaseResourceGenerator):
    resource_type = "Encounter"
    csv_file = "Encounter.csv"

    def build_from_row(self, row):
        ctx = self.context
        encounter = {
            "resourceType": "Encounter",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_ENCOUNTER_PROFILE),
            "status": ctx.csv_value(row, "status"),
            "class": ctx.build_coding(
                ctx.csv_value(row, "class_system"),
                ctx.csv_value(row, "class_code"),
                ctx.csv_value(row, "class_display"),
            ),
            "type": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "type", 1), ctx.csv_value(row, "type_text"))],
            "serviceType": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "serviceType", 1), ctx.csv_value(row, "serviceType_text")),
            "subject": self.build_subject(row),
            "participant": self.build_participants(row),
            "period": ctx.build_period_from_prefix(row, "period"),
            "reasonCode": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "reasonCode", 1), ctx.csv_value(row, "reasonCode_text"))],
            "reasonReference": [ctx.build_reference(resource_type=ctx.csv_value(row, "reasonReference_reference_type"), reference_id=ctx.csv_value(row, "reasonReference_reference_id"))],
            "diagnosis": [self.build_diagnosis(row)],
            "hospitalization": {
                "dischargeDisposition": ctx.build_codeable_concept(
                    ctx.build_codings_from_prefix(row, "dischargeDisposition", 2),
                    ctx.csv_value(row, "dischargeDisposition_text"),
                )
            },
            "location": [self.build_location(row)],
            "serviceProvider": ctx.build_reference(
                resource_type=ctx.csv_value(row, "serviceProvider_reference_type"),
                reference_id=ctx.csv_value(row, "serviceProvider_reference_id"),
                display=ctx.csv_value(row, "serviceProvider_display"),
            ),
            "description": ctx.csv_value(row, "description"),
        }
        return ctx.clean(encounter)

    def build_bulk(self, index):
        ctx = self.context
        patient_index = index
        practitioner_role_index = index
        organization_pool = max(1, ceil(self.args.count / 5))
        location_pool = max(1, ceil(self.args.count / 5))
        organization_index = ((index - 1) % organization_pool) + 1
        location_index = ((index - 1) % location_pool) + 1
        encounter = {
            "resourceType": "Encounter",
            "id": ctx.bulk_resource_id("encounter", index),
            "meta": ctx.build_meta(AU_CORE_ENCOUNTER_PROFILE),
            "status": ctx.random.choice(["planned", "in-progress", "finished"]),
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB", "display": "ambulatory"},
            "type": [{"coding": [{"system": "http://snomed.info/sct", "code": "866149003", "display": "Annual visit"}]}],
            "serviceType": {"coding": [{"system": "http://snomed.info/sct", "code": "788007007", "display": "General practice service"}]},
            "subject": {"reference": f"Patient/{ctx.bulk_resource_id('patient', patient_index)}"},
            "participant": [{"individual": {"reference": ctx.practitioner_role_reference(practitioner_role_index)}}],
            "period": {"start": ctx.faker.date_time_this_decade().isoformat()},
            "location": [{"location": {"reference": ctx.location_reference(location_index)}}],
            "serviceProvider": {"reference": ctx.organization_reference(organization_index)},
            "description": f"{ctx.random.choice(['Consultation', 'Review', 'Admission'])} encounter {index}",
        }
        return ctx.clean(encounter)

    def build_subject(self, row):
        ctx = self.context
        identifier = ctx.build_reference_identifier(row, "subject_identifier")
        if not identifier:
            identifier = None
        return ctx.build_reference(
            resource_type=ctx.csv_value(row, "subject_reference_type"),
            reference_id=ctx.csv_value(row, "subject_reference_id"),
            display=ctx.csv_value(row, "subject_display"),
            identifier=identifier,
        )

    def build_participants(self, row):
        ctx = self.context
        participants = []
        for index in (1, 2):
            type_coding = ctx.build_coding(
                ctx.csv_value(row, f"participant{index}_type_system"),
                ctx.csv_value(row, f"participant{index}_type_code"),
                ctx.csv_value(row, f"participant{index}_type_display"),
            )
            individual = None
            if index == 1:
                individual = ctx.build_reference_with_identifier(
                    row,
                    f"participant{index}_individual_reference_type",
                    f"participant{index}_individual_reference_id",
                    f"participant{index}_individual_display",
                    f"participant{index}_individual_identifier",
                )
            else:
                identifier = ctx.build_reference_identifier(row, f"participant{index}_individual_identifier")
                individual = ctx.build_reference(identifier=identifier)
            participant = ctx.clean({"type": [{"coding": [type_coding]}] if type_coding else None, "individual": individual})
            if participant:
                participants.append(participant)
        return participants

    def build_diagnosis(self, row):
        ctx = self.context
        condition = ctx.build_reference(
            resource_type=ctx.csv_value(row, "diagnosis_condition_reference_type"),
            reference_id=ctx.csv_value(row, "diagnosis_condition_reference_id"),
            display=ctx.csv_value(row, "diagnosis_condition_display"),
        )
        use = ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "diagnosis_use", 1))
        return ctx.clean({"condition": condition, "use": use})

    def build_location(self, row):
        ctx = self.context
        return ctx.clean(
            {
                "location": ctx.build_reference(
                    resource_type=ctx.csv_value(row, "location_reference_type"),
                    reference_id=ctx.csv_value(row, "location_reference_id"),
                    display=ctx.csv_value(row, "location_reference_display"),
                ),
                "status": ctx.csv_value(row, "location_status"),
            }
        )
