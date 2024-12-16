from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Hospital, Appointment, MedicalRecord
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import app  # Import the app object from app.py

# Home route to show stats (Number of Hospitals, Doctors, and Patients)
@app.route('/')
def home():
    hospitals_count = Hospital.query.count()
    doctors_count = User.query.filter_by(role='doctor').count()
    patients_count = User.query.filter_by(role='patient').count()
    return jsonify({
        'hospitals_count': hospitals_count,
        'doctors_count': doctors_count,
        'patients_count': patients_count
    })

@app.route('/hospitals', methods=['GET', 'POST'])
def manage_hospitals():
    if request.method == 'GET':
        # Get all hospitals
        hospitals = Hospital.query.all()  # Query all hospitals from the database
        hospitals_list = [
            {'id': hospital.id, 'name': hospital.name, 'location': hospital.location}
            for hospital in hospitals
        ]
        return jsonify({'hospitals': hospitals_list})
    
    if request.method == 'POST':
        # Add a new hospital
        data = request.get_json()  # Get JSON data from the request
        name = data.get('name')
        location = data.get('location')
        
        # Create a new hospital instance
        new_hospital = Hospital(name=name, location=location)
        
        # Add and commit the new hospital to the database
        db.session.add(new_hospital)
        db.session.commit()
        
        return jsonify({'message': 'Hospital created successfully', 'hospital': {'id': new_hospital.id, 'name': new_hospital.name, 'location': new_hospital.location}}), 201

# Create a New Patient
@app.route('/patients', methods=['POST'])
def create_patient():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = generate_password_hash(request.json['password'])
    
    new_patient = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role='patient'
    )
    
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient created successfully!', 'patient': {
        'id': new_patient.id,
        'first_name': new_patient.first_name,
        'last_name': new_patient.last_name,
        'email': new_patient.email
    }}), 201

# Create a New Doctor
@app.route('/doctors', methods=['POST'])
def create_doctor():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = generate_password_hash(request.json['password'])
    hospital_id = request.json['hospital_id']
    
    new_doctor = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role='doctor',
        hospital_id=hospital_id
    )
    
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor created successfully!', 'doctor': {
        'id': new_doctor.id,
        'first_name': new_doctor.first_name,
        'last_name': new_doctor.last_name,
        'email': new_doctor.email,
        'hospital_id': new_doctor.hospital_id
    }}), 201

# Get all Patients
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = User.query.filter_by(role='patient').all()
    patients_list = [
        {'id': patient.id, 'first_name': patient.first_name, 'last_name': patient.last_name, 'email': patient.email}
        for patient in patients
    ]
    return jsonify({'patients': patients_list})

# Get all Doctors
@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = User.query.filter_by(role='doctor').all()
    doctors_list = [
        {'id': doctor.id, 'first_name': doctor.first_name, 'last_name': doctor.last_name, 'email': doctor.email, 'hospital_id': doctor.hospital_id}
        for doctor in doctors
    ]
    return jsonify({'doctors': doctors_list})

@app.route('/user-info', methods=['GET'])
def get_user_info():
    try:
        # Retrieve user_id and role from the session
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401  # If no user ID, the user is not logged in

        user = User.query.get(user_id)  # Query the user based on the user_id from the session

        if user:
            user_info = {
                'id': user.id,
                'full_name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'role': user.role,
                # Role-specific additional info
            }

            if user.role == 'patient':
                user_info['additional_info'] = 'Patient-specific details'

            elif user.role == 'doctor':
                user_info['additional_info'] = 'Doctor-specific details'

            return jsonify(user_info)  # Return the user info as a JSON response

        else:
            return jsonify({'error': 'User not found'}), 404  # If user not found

    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Handle any unexpected errors


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        hospital_id = None
        
        if role == 'doctor':
            hospital_id = request.form['hospital_id']  # Get selected hospital

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role,
            hospital_id=hospital_id
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return jsonify({'message': 'Account created successfully! Please log in.'}), 201

    hospitals = Hospital.query.all()
    return jsonify({'hospitals': [hospital.name for hospital in hospitals]})

# Login Route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Get the data from the JSON request
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return jsonify({'message': 'Login successful!', 'user_id': user.id, 'role': user.role})

        else:
            flash('Invalid login credentials', 'danger')
            return jsonify({'error': 'Invalid login credentials'}), 401


# Dashboard Route (Redirect to appropriate dashboard based on user role)
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    role = session.get('role')
    
    if not user_id:
        return redirect(url_for('login'))

    if role == 'patient':
        return redirect(url_for('patient_dashboard'))
    elif role == 'doctor':
        return redirect(url_for('doctor_dashboard'))

# Patient Dashboard
@app.route('/patient_dashboard')
def patient_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    appointments = Appointment.query.filter_by(patient_id=user_id).all()
    return jsonify({'appointments': [{'id': appointment.id, 'doctor_id': appointment.doctor_id, 'date': appointment.date, 'time': appointment.time} for appointment in appointments]})

@app.route('/appointments', methods=['POST'])
def create_appointment():
    try:
        data = request.json  # Assuming JSON input for simplicity
        appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(data['time'], '%H:%M').time()
        doctor_id = data['doctor_id']
        patient_id = data['patient_id']  # Patient ID is provided in the request body

        # Create the appointment
        new_appointment = Appointment(
            date=appointment_date,
            time=appointment_time,
            patient_id=patient_id,
            doctor_id=doctor_id
        )

        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({
            'message': 'Appointment created successfully!',
            'appointment': {
                'id': new_appointment.id,
                'date': new_appointment.date,
                'time': new_appointment.time.strftime('%H:%M'),  # Ensure time is formatted
                'doctor_id': new_appointment.doctor_id,
                'patient_id': new_appointment.patient_id
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Route to get all appointments for a patient (GET)
@app.route('/appointments/patient/<int:patient_id>', methods=['GET'])
def get_appointments_by_patient(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    return jsonify([
        {
            'id': appointment.id,
            'date': appointment.date,
            'time': appointment.time.strftime('%H:%M'),  # Format time to string
            'doctor_id': appointment.doctor_id,
            'patient_id': appointment.patient_id
        } for appointment in appointments
    ])

# Route to get all appointments for a doctor (GET)
@app.route('/appointments/doctor/<int:doctor_id>', methods=['GET'])
def get_appointments_by_doctor(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([
        {
            'id': appointment.id,
            'date': appointment.date,
            'time': appointment.time.strftime('%H:%M'),  # Format time to string
            'doctor_id': appointment.doctor_id,
            'patient_id': appointment.patient_id
        } for appointment in appointments
    ])

# Route to get all appointments (GET)
@app.route('/appointments', methods=['GET'])
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify([
        {
            'id': appointment.id,
            'date': appointment.date,
            'time': appointment.time.strftime('%H:%M'),  # Format time to string
            'doctor_id': appointment.doctor_id,
            'patient_id': appointment.patient_id
        } for appointment in appointments
    ])

# Doctor Dashboard
@app.route('/doctor_dashboard')
def doctor_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    appointments = Appointment.query.filter_by(doctor_id=user_id).all()
    return jsonify({'appointments': [{'id': appointment.id, 'patient_id': appointment.patient_id, 'date': appointment.date, 'time': appointment.time} for appointment in appointments]})

@app.route('/hospitals/<int:hospital_id>/doctors', methods=['GET'])
def get_doctors_by_hospital(hospital_id):
    # Fetch doctors belonging to the specified hospital
    doctors = User.query.filter_by(hospital_id=hospital_id, role='doctor').all()
    
    # Prepare a list of doctors with relevant information
    doctors_list = [
        {'id': doctor.id, 'first_name': doctor.first_name, 'last_name': doctor.last_name, 'email': doctor.email}
        for doctor in doctors
    ]
    
    if not doctors_list:
        return jsonify({'message': 'No doctors found for this hospital'}), 404
    
    return jsonify({'doctors': doctors_list})

@app.route('/attend_appointment/<int:appointment_id>', methods=['POST'])
def attend_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Extract data from form
    diagnosis = request.form.get('diagnosis')
    treatment_plan = request.form.get('treatment_plan')
    patient_id = request.form.get('patient_id')  # Patient ID should be sent in the form data

    # Validate required fields
    if not diagnosis or not treatment_plan or not patient_id:
        return jsonify({'error': 'Diagnosis, treatment plan, and patient ID are required'}), 400

    # Create medical record
    medical_record = MedicalRecord(
        appointment_id=appointment.id,
        patient_id=patient_id,  # Use the patient_id from the form data
        diagnosis=diagnosis,
        treatment_plan=treatment_plan
    )

    db.session.add(medical_record)
    db.session.commit()

    return jsonify({
        'message': 'Medical record saved successfully!',
        'medical_record': {
            'appointment_id': medical_record.appointment_id,
            'patient_id': medical_record.patient_id,
            'diagnosis': medical_record.diagnosis,
            'treatment_plan': medical_record.treatment_plan
        }
    }), 201

@app.route('/medical_records', methods=['GET'])
def get_all_medical_records():
    try:
        # Fetch all medical records from the database
        medical_records = MedicalRecord.query.all()

        # If no records are found
        if not medical_records:
            return jsonify({'message': 'No medical records found'}), 404

        # Convert records to a list of dictionaries
        result = [{
            'id': record.id,
            'appointment_id': record.appointment_id,
            'patient_id': record.patient_id,
            'diagnosis': record.diagnosis,
            'treatment_plan': record.treatment_plan
        } for record in medical_records]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/medical_records/appointment/<int:appointment_id>', methods=['GET'])
def get_medical_records_by_appointment(appointment_id):
    try:
        # Fetch medical records filtered by appointment_id
        medical_records = MedicalRecord.query.filter_by(appointment_id=appointment_id).all()

        # If no records are found for the given appointment ID
        if not medical_records:
            return jsonify({'message': 'No medical records found for this appointment'}), 404

        # Convert records to a list of dictionaries
        result = [{
            'id': record.id,
            'appointment_id': record.appointment_id,
            'patient_id': record.patient_id,
            'diagnosis': record.diagnosis,
            'treatment_plan': record.treatment_plan
        } for record in medical_records]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
