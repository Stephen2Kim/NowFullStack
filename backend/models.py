from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'doctor' or 'patient'
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True)  # Nullable for patients

    # Relationships
    hospital = db.relationship('Hospital', back_populates='doctors')
    
    # Explicitly defining the relationships for appointments (for both patient and doctor)
    patient_appointments = db.relationship('Appointment', foreign_keys='Appointment.patient_id', back_populates='patient', lazy='dynamic')
    doctor_appointments = db.relationship('Appointment', foreign_keys='Appointment.doctor_id', back_populates='doctor', lazy='dynamic')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Hospital model
class Hospital(db.Model):
    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)

    # Relationships
    doctors = db.relationship('User', back_populates='hospital', lazy='dynamic')
    appointments = db.relationship('Appointment', back_populates='hospital')

# models.py
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    
    # Foreign Keys
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True)  # Change nullable to True

    # Relationships
    patient = db.relationship('User', foreign_keys=[patient_id], back_populates='patient_appointments')
    doctor = db.relationship('User', foreign_keys=[doctor_id], back_populates='doctor_appointments')
    hospital = db.relationship('Hospital', back_populates='appointments')

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Added patient_id column
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_plan = db.Column(db.Text, nullable=False)

    # Relationships
    appointment = db.relationship('Appointment')
    patient = db.relationship('User')  # Relationship to the User model (patient)


