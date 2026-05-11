from lib.au.builders.allergy_intolerance import AUCoreAllergyIntoleranceGenerator
from lib.au.builders.condition import AUCoreConditionGenerator
from lib.au.builders.encounter import AUCoreEncounterGenerator
from lib.au.builders.healthcare_service import AUCoreHealthcareServiceGenerator
from lib.au.builders.immunization import AUCoreImmunizationGenerator
from lib.au.builders.location import AUCoreLocationGenerator
from lib.au.builders.medication import AUCoreMedicationGenerator
from lib.au.builders.medication_request import AUCoreMedicationRequestGenerator
from lib.au.builders.medication_statement import AUCoreMedicationStatementGenerator
from lib.au.builders.observation import AUCoreObservationGenerator
from lib.au.builders.organization import AUCoreOrganizationGenerator
from lib.au.builders.patient import AUCorePatientGenerator
from lib.au.builders.practitioner import AUCorePractitionerGenerator
from lib.au.builders.practitioner_role import AUCorePractitionerRoleGenerator
from lib.au.builders.procedure import AUCoreProcedureGenerator
from lib.au.builders.related_person import AUCoreRelatedPersonGenerator


BUILDERS = {
    ("au-core-2.0.0", "allergyintolerance"): AUCoreAllergyIntoleranceGenerator,
    ("au-core-2.0.0", "condition"): AUCoreConditionGenerator,
    ("au-core-2.0.0", "encounter"): AUCoreEncounterGenerator,
    ("au-core-2.0.0", "healthcareservice"): AUCoreHealthcareServiceGenerator,
    ("au-core-2.0.0", "immunization"): AUCoreImmunizationGenerator,
    ("au-core-2.0.0", "medication"): AUCoreMedicationGenerator,
    ("au-core-2.0.0", "medicationrequest"): AUCoreMedicationRequestGenerator,
    ("au-core-2.0.0", "medicationstatement"): AUCoreMedicationStatementGenerator,
    ("au-core-2.0.0", "observation"): AUCoreObservationGenerator,
    ("au-core-2.0.0", "patient"): AUCorePatientGenerator,
    ("au-core-2.0.0", "practitioner"): AUCorePractitionerGenerator,
    ("au-core-2.0.0", "organization"): AUCoreOrganizationGenerator,
    ("au-core-2.0.0", "location"): AUCoreLocationGenerator,
    ("au-core-2.0.0", "practitionerrole"): AUCorePractitionerRoleGenerator,
    ("au-core-2.0.0", "procedure"): AUCoreProcedureGenerator,
    ("au-core-2.0.0", "relatedperson"): AUCoreRelatedPersonGenerator,
}
