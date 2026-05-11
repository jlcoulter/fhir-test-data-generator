from ..base import BaseResourceGenerator


class AUCoreObservationGenerator(BaseResourceGenerator):
    resource_type = "Observation"
    csv_file = "Observation.csv"

    def build_from_row(self, row):
        ctx = self.context
        profile_urls = [value for value in [ctx.csv_value(row, "profile1"), ctx.csv_value(row, "profile2")] if value]
        observation = {
            "resourceType": "Observation",
            "id": ctx.resource_id(row),
            "meta": {"profile": profile_urls} if profile_urls else None,
            "partOf": [ctx.build_reference(resource_type=ctx.csv_value(row, "partOf_reference_type"), reference_id=ctx.csv_value(row, "partOf_reference_id"))],
            "status": ctx.csv_value(row, "status"),
            "category": self.build_categories(row),
            "code": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "code", 2), ctx.csv_value(row, "code_text")),
            "subject": ctx.build_reference(resource_type="Patient", reference_id=ctx.csv_value(row, "subject_reference_id")),
            "encounter": ctx.build_reference(resource_type="Encounter", reference_id=ctx.csv_value(row, "encounter_reference_id"), display=ctx.csv_value(row, "encounter_display")),
            "effectiveDateTime": ctx.csv_value(row, "effectiveDateTime"),
            "performer": [self.build_performer(row)],
            "valueQuantity": ctx.build_quantity_from_prefix(row, "valueQuantity"),
            "valueCodeableConcept": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "valueCodeableConcept", 2), ctx.csv_value(row, "valueCodeableConcept_text")),
            "dataAbsentReason": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "dataAbsentReason", 1), ctx.csv_value(row, "dataAbsentReason_text")),
            "interpretation": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "interpretation1", 1))],
            "referenceRange": [self.build_reference_range(row)],
            "component": self.build_components(row),
            "hasMember": self.build_has_members(row),
            "note": [{"text": ctx.csv_value(row, "note_text")}],
            "specimen": ctx.build_reference(resource_type="Specimen", reference_id=ctx.csv_value(row, "specimen_reference_id")),
            "bodySite": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "bodySite", 1), ctx.csv_value(row, "bodySite_text")),
        }
        return ctx.clean(observation)

    def build_bulk(self, index):
        ctx = self.context
        patient_index = index
        observation = {
            "resourceType": "Observation",
            "id": ctx.bulk_resource_id("observation", index),
            "meta": {"profile": ["http://hl7.org.au/fhir/core/StructureDefinition/au-core-bodyweight"]},
            "status": "final",
            "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
            "code": {"coding": [{"system": "http://loinc.org", "code": ctx.random.choice(["29463-7", "8302-2", "8867-4"])}]},
            "subject": {"reference": f"Patient/{ctx.bulk_resource_id('patient', patient_index)}"},
            "effectiveDateTime": ctx.faker.date_this_decade().isoformat(),
            "valueQuantity": {"value": ctx.random.randint(50, 180), "unit": "kg", "system": "http://unitsofmeasure.org", "code": "kg"},
        }
        return ctx.clean(observation)

    def build_categories(self, row):
        ctx = self.context
        categories = []
        for index in (1, 2):
            category = ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, f"category{index}", 1), ctx.csv_value(row, f"category{index}_text"))
            if category:
                categories.append(category)
        return categories

    def build_performer(self, row):
        ctx = self.context
        identifier = ctx.build_reference_identifier(row, "performer1_identifier")
        return ctx.build_reference(
            resource_type=ctx.csv_value(row, "performer1_reference_type"),
            reference_id=ctx.csv_value(row, "performer1_reference_id"),
            identifier=identifier,
        )

    def build_reference_range(self, row):
        ctx = self.context
        return ctx.clean(
            {
                "low": ctx.build_quantity_from_prefix(row, "referenceRange1_low"),
                "high": ctx.build_quantity_from_prefix(row, "referenceRange1_high"),
                "type": {"text": ctx.csv_value(row, "referenceRange1_type_text")} if ctx.csv_value(row, "referenceRange1_type_text") else None,
                "text": ctx.csv_value(row, "referenceRange1_text"),
            }
        )

    def build_components(self, row):
        components = []
        for index in (1, 2, 3):
            component = self.build_component(row, index)
            if component:
                components.append(component)
        return components

    def build_component(self, row, index):
        ctx = self.context
        prefix = f"component{index}"
        return ctx.clean(
            {
                "code": ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, f"{prefix}_code", 2), ctx.csv_value(row, f"{prefix}_code_text")),
                "valueQuantity": ctx.build_quantity_from_prefix(row, f"{prefix}_valueQuantity"),
                "valueCodeableConcept": ctx.build_codeable_concept(
                    ctx.build_codings_from_prefix(row, f"{prefix}_valueCodeableConcept", 1),
                    ctx.csv_value(row, f"{prefix}_valueCodeableConcept_text"),
                ),
                "dataAbsentReason": ctx.build_codeable_concept(
                    ctx.build_codings_from_prefix(row, f"{prefix}_dataAbsentReason", 1),
                    ctx.csv_value(row, f"{prefix}_dataAbsentReason_text"),
                ),
            }
        )

    def build_has_members(self, row):
        ctx = self.context
        members = []
        for index in (1, 2):
            reference = ctx.build_reference(reference=ctx.csv_value(row, f"hasMember{index}_reference"))
            if reference:
                members.append(reference)
        return members
