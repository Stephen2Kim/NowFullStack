from datetime import datetime
from models import db, User, Hospital, Appointment

def seed_data():
    """Seeds the database with initial data."""

    # Add hospitals
    hospital1 = Hospital(name='St Famille International Hospital', location='Butare')
    hospital2 = Hospital(name='Amahoro Level 3 General Hospital', location='Gisenyi')
    hospital3 = Hospital(name='Lake Kivu Teaching and Referal Hospital', location='Kibuye')
    hospital4 = Hospital(name='Pfunda General Residency Hospital', location='Kagitumba')
    hospital5 = Hospital(name='Kigali Cancer Institution', location='Muhanga')
    hospital6 = Hospital(name='Mwima Mausoleum Level 5 Hospital', location='Ruhengeri')
    db.session.add_all([hospital1, hospital2, hospital3, hospital4, hospital5, hospital6])
    db.session.commit()

    # Add doctors
    doctor1 = User(first_name='Meridith', last_name='Grey', email='mergrey15@gmail.com', password='hashedpassword1', role='doctor', hospital_id=hospital1.id)
    doctor2 = User(first_name='Alex', last_name='Karev', email='Alkar15@gmail.com', password='hashedpassword2', role='doctor', hospital_id=hospital2.id)
    doctor3 = User(first_name='Derek', last_name='Shepherd', email='dersheph15@gmail.com', password='hashedpassword1', role='doctor', hospital_id=hospital3.id)
    doctor4 = User(first_name='Arizona', last_name='Robins', email='Arrobbin15@gmail.com', password='hashedpassword2', role='doctor', hospital_id=hospital4.id)
    doctor5 = User(first_name='Callie', last_name='Torres', email='caltorr15@gmail.com', password='hashedpassword1', role='doctor', hospital_id=hospital5.id)
    doctor6 = User(first_name='Christina', last_name='Yang', email='chriyan15@mgmail.com', password='hashedpassword2', role='doctor', hospital_id=hospital6.id)
    doctor7 = User(first_name='Addison', last_name='Montgomery', email='addimon15@gmail.com', password='hashedpassword1', role='doctor', hospital_id=hospital1.id)
    doctor8 = User(first_name='Izzie', last_name='Stevens', email='izzste15@gmail.com', password='hashedpassword2', role='doctor', hospital_id=hospital2.id)
    doctor9 = User(first_name='Mark', last_name='Sloan', email='masloan15@gmail.com', password='hashedpassword1', role='doctor', hospital_id=hospital3.id)
    doctor10 = User(first_name='Miranda', last_name='Bailey', email='mirbail15@gmail.com', password='hashedpassword2', role='doctor', hospital_id=hospital4.id)
    doctor11 = User(first_name='Teddy', last_name='Altman', email='tedalman15@gmail.com', password='hashedpassword1', role='doctor', hospital_id=hospital5.id)
    doctor12 = User(first_name='Lexie', last_name='Grey', email='lexey15@gmail.com', password='hashedpassword2', role='doctor', hospital_id=hospital6.id)
    db.session.add_all([doctor1, doctor2, doctor3, doctor4, doctor5, doctor6, doctor7, doctor8, doctor9, doctor10, doctor11, doctor12])
    db.session.commit()

    # Add patients
    patient1 = User(first_name='Andrew', last_name='Deluca', email='andreluca@gmail.com', password='hashedpassword3', role='patient')
    patient2 = User(first_name='Henry', last_name='Burton', email='henrurton@gmail.com', password='hashedpassword4', role='patient')
    db.session.add_all([patient1, patient2])
    db.session.commit()

    # Add appointments
    appointment1 = Appointment(
        date=datetime.strptime('2024-12-20', '%Y-%m-%d').date(),
        time=datetime.strptime('10:30', '%H:%M').time(),
        patient_id=patient1.id,
        doctor_id=doctor1.id
    )
    db.session.add(appointment1)
    db.session.commit()

    print("Database seeded successfully!")
