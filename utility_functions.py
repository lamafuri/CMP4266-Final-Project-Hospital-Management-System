from Doctor import Doctor
from Patient import Patient
def update_file(objects_list , filename):
    folder_name = './Data/'
    """Function to update the text file entirely"""
    try:
        with open(folder_name+filename , 'w') as file:
            for obj in objects_list:
                file.write(obj.to_csv_format()+'\n')
    except Exception as e:
        print("Save Error :",e)

def load_doctors_data():
    """Load all the information saved in docotor.txt and return list of Doctor objects"""
    doctors = []
    try:
        with open('./Data/doctor.txt','r') as file:
            row = file.readline()
            while row:
                list_of_row_values = row.split(',')
                first_name , surname , speciality = list_of_row_values
                doctors.append(Doctor(first_name , surname , speciality.strip()))
                row = file.readline()

    except Exception as e:
        print("Error Loading docotor data \n    Error : ",e)

    else:
        return doctors
    
def load_patients_data():
    """Load all the information saved in patient.txt and return list of Patient Object and dictionary representated as a family name : patients list"""
    patients = []
    grouped_patients = {}

    try:
        with open('./Data/patient.txt','r') as file:
            row = file.readline()
            while row:
                list_of_row_values = row.split(',')
                first_name , surname , age , mobile , postcode , doctor_full_name = list_of_row_values
                current_patient = Patient(first_name , surname , age , mobile , postcode)
                current_patient.link(doctor_full_name.strip())
                patients.append(current_patient)
                surname = current_patient.get_surname()
                grouped_patients.setdefault(surname,[]).append(current_patient)
                row = file.readline()

    except Exception as e:
        print("Error Loading patients data \n    Error : ",e)

    else:
        print(len(grouped_patients))
        return patients , grouped_patients
    
def load_discharged_patients_data():
    """Load all the information saved in discharged_patient.txt and return list of Patient objects"""
    discharged_patients = []
    try:
        with open('./Data/discharged_patient.txt','r') as file:
            row = file.readline()
            while row:
                list_of_row_values = row.split(',')
                first_name , surname , age , mobile , postcode , doctor_full_name = list_of_row_values
                current_patient = Patient(first_name , surname , age , mobile , postcode)
                current_patient.link(doctor_full_name.strip())
                discharged_patients.append(current_patient)
                row = file.readline()

    except Exception as e:
        print("Error Loading discharged patients data \n    Error : ",e)

    else:
        return discharged_patients

def update_patients_list_in_doctor(doctor_by_name , patients):
    for patient in patients:
        doctor_name = patient.get_doctor()
        if(doctor_name != 'None' and doctor_name in doctor_by_name):
            doctor = doctor_by_name[doctor_name]
            doctor.add_patient(patient)


if __name__ =='__main__':
    x = load_patients_data()
    print(x)
   