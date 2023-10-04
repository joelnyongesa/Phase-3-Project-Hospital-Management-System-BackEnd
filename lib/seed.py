from faker import Faker
import random

from models import Doctor, Nurse, Patient, Ward
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


fake = Faker()

if __name__ == "__main__":
    engine = create_engine("sqlite:///database.db")
    Session = sessionmaker(bind=engine)
    session = Session()


    session.query(Doctor).delete()
    session.query(Nurse).delete()
    session.query(Patient).delete()
    session.query(Ward).delete()


    # doctor specialization
    specializations = ["Cardiology", "Dermatology", "Gastroenterology", "Neurology", 
                   "Orthopedics", "Pediatrics", "Oncology", "Psychiatry", 
                   "Radiology", "Urology"]

    doctors = []
    for i in range(10):
        doctor = Doctor(
            name = fake.name(),
            specialization = random.choice(specializations)
        )
        session.add(doctor)
        session.commit()

        doctors.append(doctor)

    nurses = []
    for i in range(15):
        nurse = Nurse(
            name = fake.name(),
            doctor_id = random.randint(1,10),
            patient_id = random.randint(1,51)
        )
        session.add(nurse)
        session.commit()

        nurses.append(nurse)

    patients = []
    for i in range(50):
        patient = Patient(
            name = fake.name(),
            doctor_id = random.randint(1,10),
            nurse_id = random.randint(1,15),
            ward_id = random.randint(1,10),
        )

        session.add(patient)
        session.commit()
        
        patients.append(patient)

    wards = []
    for i in range(10):
        ward = Ward(
            name = f"{fake.name()} Ward"
        )
        session.add(ward)
        session.commit()
