from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
import click

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Many to many relationships between nurses and patients
nurses_patients = Table(
    "nurses_patients",
    Base.metadata,
    Column(
        "nurse_id",
        Integer,
        ForeignKey("nurses.id"),
        primary_key=True
    ),
    Column(
        "patient_id",
        Integer,
        ForeignKey("patients.id"),
        primary_key=True
    ),
    extend_existing=True
)


# Creating our models
class Doctor(Base):
    __tablename__ = "doctors"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialization = Column(String)

    # relationships
    nurses = relationship("Nurse", backref=backref('doctors'))
    patients = relationship("Patient", backref=backref("doctor"))

    # CLASS METHODS
    @classmethod
    def doctor_details(cls, doctor_id):
        # Returns the details about a specific doctor, searches by ID
        result = session.query(Doctor).filter_by(id=doctor_id).first()
        if result is not None:
            return result
        return f"Doctor with TBora ID {doctor_id} not found!"
    
    @classmethod
    def get_patients(cls, doctor_id):
        patients =  session.query(Patient).join(Doctor, onclause=Doctor.id == Patient.doctor_id).filter(Doctor.id == doctor_id).all()
        if patients is not None:
            print(f"Patients for Doctor {doctor_id}")
            for patient in patients:
                print(patient)
        else:
            print (f"No patients found for Doctor {doctor_id}")

    @classmethod
    def get_nurses(cls, doctor_id):
        nurses = session.query(Nurse).join(Doctor, onclause=Nurse.doctor_id == Doctor.id).filter(Doctor.id == doctor_id).all()
        if nurses is not None:
            print(f"Nurses assigned to Doctor {doctor_id}")
            for nurse in nurses:
                print(nurse)
        else:
            print(f"No nurses are currently assigned to doctor{doctor_id}")
    
    def __repr__(self):
        return f"Doctor id ({self.id}), "\
            f"Name: {self.name}, "\
            f"Specialization: {self.specialization}"

    
class Nurse(Base):
    __tablename__ = "nurses"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))

    # Relationships
    patients = relationship("Patient", secondary=nurses_patients, back_populates="nurses")

    # CLASS METHODS
    @classmethod
    def get_details(cls, nurse_id) :
        nurse =  session.query(Nurse).filter(Nurse.id == nurse_id).first()

        if nurse is not None:
            return nurse
        return f"Nurse with TBora ID {nurse_id} not found!"
    
    @classmethod
    def get_doctor(cls, nurse_id):
        nurse_doctor = session.query(Doctor).join(Nurse, onclause=Doctor.id == Nurse.doctor_id).filter(Nurse.id == nurse_id).first()

        if nurse_doctor is not None:
            return nurse_doctor
        return f"No doctor has nurse {nurse_id} assigned!"
    
    @classmethod
    def get_patients(cls, nurse_id):
        patients = session.query(Patient).join(nurses_patients).filter(nurses_patients.c.nurse_id == nurse_id).all()
        if patients is not None:
            print(f"Patients for nurse {nurse_id}")
            for patient in patients:
                return (patient)
        return f"No patients for nurse {nurse_id}"

    def __repr__(self):
        return f"Nurse id ({self.id}), "+\
            f"Name: {self.name}"
    
class Patient(Base):
    __tablename__ = "patients"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))

    # relationships
    nurses = relationship("Nurse", secondary=nurses_patients, back_populates="patients")

    # CLASS METHODS
    @classmethod
    def get_details(cls, patient_id):
        patient = session.query(Patient).filter_by(id = patient_id).first()
        if patient is not None:
            return patient
        return f"Patient Adm Number {patient_id} not found!"
    
    @classmethod
    def get_doctor(cls, patient_id):
        doctor = session.query(Doctor).join(Patient, onclause=Patient.doctor_id == Doctor.id).filter(Patient.id == patient_id).first()

        if doctor is not None:
            return doctor
        
        return f"No doctor assigned to patient {patient_id}"
    
    @classmethod
    def get_nurses(cls, patient_id):
        nurses = session.query(Nurse).join(nurses_patients).filter(nurses_patients.c.patient_id == patient_id).all()

        if nurses:
            print(f"Nurse(s) assigned to patient ({patient_id}):")
            for nurse in nurses:
                print(nurse)
        else:
            print(f"No nurses assigned to patient {patient_id}")

    @classmethod
    def get_ward(cls, patient_id):
        ward = session.query(Ward).join(Patient, onclause=Patient.ward_id == Ward.id).filter(Patient.id == patient_id).first()
        if ward is not None:
            return ward
        else:
            return f"No ward founc for patient {patient_id}"


    def __repr__(self):
        return f"Patient Reg Number: ({self.id}), "\
            f"Patient name: {self.name}"\

class Ward(Base):
    __tablename__ = "wards"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # relationships
    patients = relationship("Patient", backref=backref("ward"))

    # CLASS METHODS
    @classmethod
    def get_details(cls, ward_id):
        return session.query(Ward).filter(Ward.id == ward_id).first()

    @classmethod
    def number_of_patients(cls, ward_id):
        num_patients = session.query(func.count(Patient.id)).filter_by(ward_id=ward_id).scalar()
        return f"Ward {ward_id} currently has {num_patients} patients admitted!"


    def __repr__(self):
        return f"Ward ID({self.id}), "\
            f"Ward name: {self.name}"
    



class HospitalManagement:
    def __init__(self):
        pass

    def main_menu(self):
        while True:
            click.echo("Welcome to Tiba Bora Hospital")
            choice = click.prompt("Please select an option\n1. Doctors.\n2. Nurses.\n3. Patients\n4. Wards\n(Q or q to quit)\nSelect an option", type=str)
            
            if choice.lower() == 'q':
                break

            if choice == '1':
                self.doctor_menu()
            elif choice == '2':
                self.nurse_menu()
            elif choice == '3':
                self.patient_menu()
            elif choice == '4':
                self.ward_menu()
            else:
                click.echo("Invalid option, please try again!")

    def doctor_menu(self):
        sub_option = click.prompt("What would you like to do?\n1. Get details of a doctor.\n2. See nurses assigned to a particular doctor.\n3. See patients for a particular doctor\nSelect an option", type=int)

        if sub_option == 1:
            doctor_id = click.prompt("Enter TBora ID for the doctor you want to search", type=int)
            print(Doctor.doctor_details(doctor_id))
        elif sub_option == 2:
            doctor_id = click.prompt("Enter TBora ID for doctor to get the nurses under the doctor", type=int)
            Doctor.get_nurses(doctor_id)
        elif sub_option == 3:
            doctor_id = click.prompt("Enter TBora ID for doctor to retrieve the patients for the doctor")
            Doctor.get_patients(doctor_id)
        else:
            print("Invalid option selected!")
    def nurse_menu(self):
        sub_option = click.prompt("What would you like to do?\n1.Get nurse details using TBora ID\n2. See doctor a particular nurse reports to.\n3. View patients assigned to a specific nurse\nSelect an option", type=int)

        if sub_option == 1:
            nurse_id = click.prompt("Enter TBora ID for the nurse to get the full details", type=int)
            print(Nurse.get_details(nurse_id))
        elif sub_option == 2:
            nurse_id = click.prompt("Enter TBora ID for nurse to get the doctor assigned the nurse", type=int)
            print(Nurse.get_doctor(nurse_id))
        elif sub_option == 3:
            nurse_id = click.prompt("Enter TBora ID for nurse to see patients assigned to a particular nurse", type=int)
            print(Nurse.get_patients(nurse_id))
        else:
            print("Invalid option!")
    
    def patient_menu(self):
        sub_option = click.prompt("What would you like to do?\n1. Get details of a particular patient.\n2. See the doctor assigned to a patient\n3. See nurses assigned to a patient\n4. See ward a patient is admitted to\nSelect an option", type=int)

        if sub_option == 1:
            patient_id = click.prompt("Enter patient admission number", type=int)
            print(Patient.get_details(patient_id))
        elif sub_option == 2:
            patient_id = click.prompt("Enter patient admission number to see the doctor", type=int)
            print(Patient.get_doctor(patient_id))
        elif sub_option == 3:
            patient_id = click.prompt("Enter patient admission number to get the nurse(s) assigned to a patient", type=int)
            print(Patient.get_nurses(patient_id))
        elif sub_option == 4:
            patient_id = click.prompt("Enter patient admission number to see the ward patient is admitted to",type=int)
            print(Patient.get_ward(patient_id))
        else:
            print("Invalid option, try again!")

    def ward_menu(self):
        sub_option = click.prompt("What would you like to do?\n1. Get details of a particular ward.\n2. See the total number of patients admitted in a particular ward.\nSelect an option", type=int)

        if sub_option == 1:
            ward_id = click.prompt("Enter ward number", type=int)
            print(Ward.get_details(ward_id))
        elif sub_option == 2:
            ward_id = click.prompt("Enter ward number", type=int)
            print(Ward.number_of_patients(ward_id))
        else:
            print("Invalid option, try again!")

@click.command()
def main():
    hospital_management = HospitalManagement()
    hospital_management.main_menu()

if __name__ == "__main__":
    main()