import json
import random
from faker import Faker

# Initialize Faker for generating random text
fake = Faker()

# Load the new JSON file
input_file = "Templates For Data Generation/documents_queries.json"  # Replace with your file path
output_file = "Generated Data/generated_documents.json"

with open(input_file, 'r') as f:
    data = json.load(f)

# Define a function to create variations for a single query and its entity
def generate_variations(query, entity_substitutions, num_variations=8):
    variations = []
    for substitution in entity_substitutions:
        for _ in range(num_variations):
            # Replace entity in the query with the substitution
            new_query = query.replace(entity, substitution)
            # Add some randomness using Faker
            random_variation = fake.sentence(nb_words=random.randint(5, 12)).replace('.', '')
            variations.append(random_variation.replace(entity, substitution))
    return variations

# Define entity substitutions (manual or simple substitutions)
entity_substitution_map = {
    "academic calendar": ["calendar of academics", "school calendar"],
    "tuition fee payment deadline": ["payment deadline for tuition", "last day to pay tuition fees"],
    "dormitory application": ["application for dorms", "dorm registration form"],
    "class schedule": ["schedule of classes", "timetable for classes"],
    "student library discount": ["library discount for students", "student discount at the library"],
    "CS101 syllabus": ["syllabus for CS101", "CS101 course syllabus"],
    "library opening hours": ["library operating hours", "library hours of operation"],
    "student ID card": ["student identification card", "university ID card"],
    "late payment rules": ["rules for late payments", "late payment policies"],
    "student parking policy": ["parking policy for students", "student parking rules"],
    "class drop deadline": ["deadline for dropping a class", "last day to drop a class"],
    "course catalog": ["catalog of courses", "list of available courses"],
    "scholarship application procedure": ["procedure for scholarship application", "scholarship application process"],
    "check grades online": ["view grades online", "online grade access"],
    "exam schedule": ["schedule of exams", "exam timetable"],
    "course registration deadline": ["deadline for course registration", "last day to register for courses"],
    "financial aid documents": ["documents for financial aid", "financial aid paperwork"],
    "update contact information": ["update personal contact information", "change contact details"],
    "transcript": ["official transcript", "academic transcript"],
    "international student documents": ["documents for international students", "international student requirements"],
    "late application submission": ["submit application late", "late application submission procedure"],
    "student handbook": ["handbook for students", "student guidebook"],
    "school code of conduct": ["code of conduct for students", "university conduct guidelines"],
    "change major procedure": ["procedure for changing major", "major change process"],
    "student health insurance policy": ["policy for student health insurance", "health insurance for students"],
    "on-campus housing application": ["application for on-campus housing", "dormitory application"],
    "class refund policy": ["refund policy for classes", "class refund procedures"],
    "grade report online access": ["access grade report online", "online access to grade report"],
    "internship application process": ["process for applying to internships", "internship application procedure"],
    "student support center location": ["location of student support center", "student support center address"],
    "graduation requirements document": ["document for graduation requirements", "graduation requirement guidelines"],
    "next semester start date": ["start date for next semester", "beginning of next semester"],
    "library services information": ["information about library services", "library services details"],
    "course substitution rules": ["rules for substituting courses", "course substitution policy"],
    "student parking permit": ["permit for student parking", "student parking pass"],
    "class withdrawal procedure": ["procedure for withdrawing from a class", "class withdrawal policy"],
    "financial aid application form": ["form for financial aid application", "financial aid application"],
    "course transcript": ["transcript for course", "academic course transcript"],
    "student loans available": ["available student loans", "student loan options"],
    "student records online access": ["access student records online", "online student records"],
    "graduate program application": ["application for graduate programs", "apply for graduate programs"],
    "grading system explanation": ["explanation of grading system", "grading policy"],
    "scholarship requirements": ["requirements for scholarships", "scholarship eligibility"],
    "campus events information": ["information on campus events", "campus event details"],
    "online billing statement": ["billing statement online", "access online billing statement"],
    "leave of absence rules": ["rules for taking a leave of absence", "leave of absence policy"],
    "academic policies": ["policies for academics", "university academic policies"],
    "university withdrawal procedure": ["procedure for university withdrawal", "withdrawing from university"],
    "financial aid application": ["application for financial aid", "process for financial aid application"],
    "student discounts": ["available student discounts", "discounts for students"],
    "career services office location": ["location of career services office", "career services office address"],
    "faculty policies document": ["document for faculty policies", "faculty policy guidelines"],
    "on-campus employment application": ["application for on-campus employment", "on-campus job application"],
    "replacement student ID card": ["replacement for student ID card", "get a new student ID card"],
    "add class procedure": ["procedure for adding a class", "adding a class process"],
    "student schedule": ["personal student schedule", "student class schedule"],
    "course complaint submission": ["submit a complaint about a course", "course complaint process"],
    "grade appeal procedure": ["procedure for appealing a grade", "grade appeal process"],
    "course material refund": ["refund for course materials", "refund on course materials"],
    "student directory access": ["access to student directory", "student directory information"],
    "next orientation session date": ["date for next orientation session", "next orientation session details"],
    "summer session application deadline": ["deadline for summer session application", "summer session application cutoff"],
    "student conduct policy document": ["document for student conduct policy", "student conduct policy guidelines"],
    "refund request form": ["form for refund request", "refund request application"],
    "exchange program application": ["application for exchange program", "exchange program application process"],
    "student activity fee document": ["document for student activity fee", "student activity fee details"],
    "next semester tuition payment deadline": ["tuition payment deadline for next semester", "next semester tuition payment due date"],
    "student code of conduct": ["student conduct code", "code of student conduct"],
    "dormitory assignment switch": ["switch dormitory assignment", "change dormitory room"],
    "student financial aid office location": ["location of student financial aid office", "student financial aid office address"],
    "student loan application": ["application for student loan", "student loan process"],
    "course withdrawal form": ["form for course withdrawal", "withdrawal form for courses"],
    "gap year policy": ["policy for taking a gap year", "gap year guidelines"],
    "student tutoring center location": ["location of student tutoring center", "student tutoring center address"],
    "credit transfer policy": ["policy on credit transfer", "credit transfer procedure"],
    "student housing requirements": ["requirements for student housing", "student housing eligibility"],
    "exam results online access": ["access exam results online", "online access to exam results"],
    "graduation application deadline": ["deadline for graduation application", "graduation application due date"],
    "course schedule change procedure": ["procedure for changing course schedule", "changing course schedule"],
    "student wellness center location": ["location of student wellness center", "student wellness center address"],
    "student grievance procedure": ["procedure for student grievance", "grievance procedure for students"],
    "campus housing application": ["application for campus housing", "apply for campus housing"],
    "university mission statement document": ["document for university mission statement", "university mission statement details"]
}


# Iterate through data and generate variations
output_data = []
for item in data:
    intent = item["Intent"]
    query = item["Query"]
    entities = item["Entities"]

    for entity in entities:
        if entity in entity_substitution_map:
            substitutions = entity_substitution_map[entity]
            variations = generate_variations(query, substitutions)
            for variation in variations:
                output_data.append({
                    "Intent": intent,
                    "Query": variation,
                    "Entities": [entity]
                })

# Save the generated variations to a new JSON file
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Generated variations saved to {output_file}")
