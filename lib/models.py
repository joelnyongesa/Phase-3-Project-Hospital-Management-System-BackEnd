from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
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
    nurses = relationship("Nurse", backref=backref('doctor_nurse'))
    patients = relationship("Patient", backref=backref("doctor_patient"))

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
    patient_id = Column(Integer, ForeignKey("patients.id"))

    # Relationships
    patients = relationship("Patient", secondary=nurses_patients, back_populates="nurses")

    def __repr__(self):
        return f"Nurse id ({self.id}), "+\
            f"Name: {self.name}"
    
class Patient(Base):
    __tablename__ = "patients"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    nurse_id = Column(Integer, ForeignKey("nurses.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))

    # relationships
    nurses = relationship("Nurse", secondary=nurses_patients, back_populates="patients")

    def __repr__(self):
        return f"Patient ID: ({self.id}), "\
            f"Patient name: {self.name}"

class Ward(Base):
    __tablename__ = "wards"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # relationships
    patients = relationship("Patient", backref=backref("ward_patient"))

    def __repr__(self):
        return f"Ward ID({self.id}), "\
            f"Ward name: {self.name}"
    


    # Defining the class methods
    