from ..base import BaseResourceGenerator


AU_CORE_RELATED_PERSON_PROFILE = "http://hl7.org.au/fhir/core/StructureDefinition/au-core-relatedperson"


class AUCoreRelatedPersonGenerator(BaseResourceGenerator):
    resource_type = "RelatedPerson"
    csv_file = "RelatedPerson.csv"

    def build_from_row(self, row):
        ctx = self.context
        related_person = {
            "resourceType": "RelatedPerson",
            "id": ctx.resource_id(row),
            "meta": ctx.build_meta(AU_CORE_RELATED_PERSON_PROFILE),
            "identifier": self.build_identifiers(row),
            "patient": ctx.build_reference(resource_type="Patient", reference_id=ctx.csv_value(row, "patient_reference_id")),
            "relationship": [ctx.build_codeable_concept(ctx.build_codings_from_prefix(row, "relationship", 1))],
            "name": [
                ctx.build_human_name(
                    use=ctx.csv_value(row, "name1_use"),
                    family=ctx.csv_value(row, "name1_family"),
                    given=[value for value in [ctx.csv_value(row, "name1_given1"), ctx.csv_value(row, "name1_given2")] if value],
                )
            ],
            "gender": ctx.csv_value(row, "gender"),
            "birthDate": ctx.csv_value(row, "birthDate"),
            "telecom": self.build_telecoms(row),
            "address": [
                ctx.build_address(
                    line=[ctx.csv_value(row, "address1_line1")] if ctx.csv_value(row, "address1_line1") else [],
                    city=ctx.csv_value(row, "address1_city"),
                    state=ctx.csv_value(row, "address1_state"),
                    postal_code=ctx.csv_value(row, "address1_postalCode"),
                    country=ctx.csv_value(row, "address1_country"),
                )
            ],
            "extension": self.build_extensions(row),
        }
        return ctx.clean(related_person)

    def build_bulk(self, index):
        ctx = self.context
        patient_index = index
        given_name = ctx.faker.first_name_female()
        family_name = ctx.faker.last_name()
        related_person = {
            "resourceType": "RelatedPerson",
            "id": ctx.bulk_resource_id("relatedperson", index),
            "meta": ctx.build_meta(AU_CORE_RELATED_PERSON_PROFILE),
            "patient": {"reference": f"Patient/{ctx.bulk_resource_id('patient', patient_index)}"},
            "relationship": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode", "code": "MTH", "display": "mother"}]}],
            "name": [{"use": "official", "family": family_name, "given": [given_name]}],
            "gender": "female",
            "birthDate": ctx.faker.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "telecom": [{"system": "phone", "use": "mobile", "value": ctx.faker.phone_number()}],
        }
        return ctx.clean(related_person)

    def build_identifiers(self, row):
        identifiers = []
        for index in (1, 2):
            identifier = self.context.build_identifier_from_prefix(row, f"identifier{index}")
            if identifier:
                extensions = []
                status_code = self.context.csv_value(row, f"identifier{index}_ihiStatus_code")
                record_status_code = self.context.csv_value(row, f"identifier{index}_ihiRecordStatus_code")
                if status_code:
                    extensions.append({"url": "http://hl7.org.au/fhir/StructureDefinition/ihi-status", "valueCode": status_code})
                if record_status_code:
                    extensions.append({"url": "http://hl7.org.au/fhir/StructureDefinition/ihi-record-status", "valueCode": record_status_code})
                if extensions:
                    identifier["extension"] = extensions
                identifiers.append(identifier)
        return identifiers

    def build_telecoms(self, row):
        telecoms = []
        for index in (1, 2, 3):
            telecom = self.context.build_telecom(
                system=self.context.csv_value(row, f"telecom{index}_system"),
                use=self.context.csv_value(row, f"telecom{index}_use"),
                value=self.context.csv_value(row, f"telecom{index}_value"),
            )
            if telecom:
                telecoms.append(telecom)
        return telecoms

    def build_extensions(self, row):
        ctx = self.context
        extensions = []
        if ctx.csv_value(row, "individual_genderIdentity_value_code") or ctx.csv_value(row, "individual_genderIdentity_value_display"):
            extensions.append(
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/individual-genderIdentity",
                    "extension": [
                        {
                            "url": "value",
                            "valueCodeableConcept": ctx.build_codeable_concept(
                                [ctx.build_coding("http://snomed.info/sct", ctx.csv_value(row, "individual_genderIdentity_value_code"), ctx.csv_value(row, "individual_genderIdentity_value_display"))]
                            ),
                        }
                    ],
                }
            )
        if ctx.csv_value(row, "individual_pronouns_value_code") or ctx.csv_value(row, "individual_pronouns_value_display"):
            extensions.append(
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/individual-pronouns",
                    "extension": [
                        {
                            "url": "value",
                            "valueCodeableConcept": ctx.build_codeable_concept(
                                [ctx.build_coding("http://loinc.org", ctx.csv_value(row, "individual_pronouns_value_code"), ctx.csv_value(row, "individual_pronouns_value_display"))]
                            ),
                        }
                    ],
                }
            )
        if ctx.csv_value(row, "individual_recordedSexOrGender_type_code") or ctx.csv_value(row, "individual_recordedSexOrGender_value_code"):
            extensions.append(
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/individual-recordedSexOrGender",
                    "extension": [
                        {
                            "url": "type",
                            "valueCodeableConcept": ctx.build_codeable_concept(
                                [ctx.build_coding("http://loinc.org", ctx.csv_value(row, "individual_recordedSexOrGender_type_code"))],
                                ctx.csv_value(row, "individual_recordedSexOrGender_type_text"),
                            ),
                        },
                        {
                            "url": "value",
                            "valueCodeableConcept": ctx.build_codeable_concept(
                                [ctx.build_coding("http://snomed.info/sct", ctx.csv_value(row, "individual_recordedSexOrGender_value_code"))],
                                ctx.csv_value(row, "individual_recordedSexOrGender_value_text"),
                            ),
                        },
                    ],
                }
            )
        return extensions
