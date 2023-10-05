from faker import Faker
import random
from models import Doctor, Nurse, Patient, Ward, nurses_patients
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

fake = Faker()

if __name__ == "__main__":
    engine = create_engine("sqlite:///database.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.query(Doctor).delete()
    session.query(Nurse).delete()
    session.query(Patient).delete()
    session.query(Ward).delete()

    # List of doctor specializations
    specializations = ["Cardiology", "Dermatology", "Gastroenterology", "Neurology", 
                       "Orthopedics", "Pediatrics", "Oncology", "Psychiatry", 
                       "Radiology", "Urology"]

    doctors = []
    for _ in range(10):
        doctor = Doctor(
            name=fake.name(),
            specialization=random.choice(specializations)
        )
        session.add(doctor)
        session.commit()
        doctors.append(doctor)

    nurses = []
    for _ in range(15):
        nurse = Nurse(
            name=fake.name(),
            doctor_id=random.randint(1, 10),
            patient_id=random.randint(1, 51)
        )
        session.add(nurse)
        session.commit()
        nurses.append(nurse)

    patients = []
    for _ in range(50):
        patient = Patient(
            name=fake.name(),
            doctor_id=random.randint(1, 10),
            nurse_id=random.randint(1, 15),
            ward_id=random.randint(1, 10),
        )
        session.add(patient)
        session.commit()
        patients.append(patient)

    wards = []
    for _ in range(10):
        ward = Ward(
            name=f"{fake.word()} Ward"
        )
        session.add(ward)
        session.commit()
        wards.append(ward)

    # Populate the association table nurses_patients
    for nurse in nurses:
        # Random number of patients each nurse is assigned to
        num_patients = random.randint(1, 5)
        # Randomly select patients to assign to the nurse
        patients_to_assign = random.sample(patients, num_patients)
        # Add nurse-patient relationships to the association table
        nurse.patients.extend(patients_to_assign)
        session.commit()

    session.close()

