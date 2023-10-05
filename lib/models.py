from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref

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
        return session.query(Doctor).filter_by(id=doctor_id).first()
    
    @classmethod
    def get_patients(cls, doctor_id):
        patients =  session.query(Patient.name).join(Doctor, onclause=Doctor.id == Patient.doctor_id).filter(Doctor.id == doctor_id).all()
        if patients is not None:
            print(f"Patients for Doctor {doctor_id}")
            for patient in patients:
                print(patient)
        else:
            print (f"No patients found for Doctor ID {doctor_id}")

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
        return f"Nurse {nurse_id} not found!"
    
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
        return f"Patient {patient_id} not found!"
    
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
        return f"Patient ID: ({self.id}), "\
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
        return session.query(Ward).filter(Ward.id == ward_id)

    @classmethod
    def number_of_patients(cls, ward_id):
        num_patients = session.query(func.count(Patient.id)).filter_by(ward_id=ward_id).scalar()
        return f"Ward {ward_id} currently has {num_patients} patients admitted!"


    def __repr__(self):
        return f"Ward ID({self.id}), "\
            f"Ward name: {self.name}"
    


    
    