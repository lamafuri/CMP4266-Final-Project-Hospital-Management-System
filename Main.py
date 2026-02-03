# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
from utility_functions import load_doctors_data , load_patients_data , load_discharged_patients_data , update_patients_list_in_doctor , save_appointment , load_appointments
def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors
    admin = Admin.load_admin_data() # username is 'admin', password is '000'

    # doctors = [Doctor('John','Smith','Internal Med.'), Doctor('Jone','Smith','Pediatrics'), Doctor('Jone','Carlos','Cardiology')]
    doctors = load_doctors_data()
    # patients = [Patient('Sara','Smith', 20, '07012345678','B1 234'), Patient('Mike','Jones', 37,'07555551234','L2 2AB'), Patient('Daivd','Smith', 15, '07123456789','C1 ABC')]
    patients , grouped_patients = load_patients_data()
    # discharged_patients = []
    discharged_patients = load_discharged_patients_data()

    doctor_by_name = {doctor.full_name(): doctor for doctor in doctors}
    update_patients_list_in_doctor(doctor_by_name , patients)
    load_appointments(doctors)
    # keep trying to login tell the login details are correct
    while True:
        # Successful login only if there was no exception raised
        try:
            admin.login()
        except Exception as e:
            print(e)
        else:
            running = True #allow the program to run
            break


    while running:
        # print the menu
        print('Choose the operation:')
        print(' 1- Register/view/update/delete doctor')
        print(' 2- Admit/View/Discharge Patients')
        print(' 3- View discharged patient')
        print(' 4- Assign doctor to a patient')
        print(' 5- Reallocate Doctor to Patient')
        print(' 6- View Management Report')
        print(' 7- Update admin detais')
        print(" 8- View Grouped Patient's By Family")
        print(" 9- Make an appointment")
        print(' 10- Quit')

        # get the option
        op = input('Option: ')

        if op == '1':
            # 1- Register/view/update/delete doctor
            #ToDo1
            admin.doctor_management(doctors)

        elif op == '2':
            # 2- Admit / View / discharge patients
            #ToDo2
            print("    1. Admit new Patient\n    2. View Patients\n    3. Discharge Patient")
            operation = input("Enter the operation : ")
            if operation == '1':
                admin.admit_patient(patients)
            elif operation == '2':
                admin.view_patient(patients)
            
            elif operation == '3':
                while True:
                    op = input('Do you want to discharge a patient(Y/N):').lower()

                    if op == 'yes' or op == 'y':
                        #ToDo3
                        admin.view_patient(patients)
                        admin.discharge(patients , discharged_patients)

                    elif op == 'no' or op == 'n':
                        break

                    # unexpected entry
                    else:
                        print('Please answer by yes or no.')
            else:
                print("Invalid Operation ! 1,2,3 are only valid")
        elif op == '3':
            # 3 - view discharged patients
            #ToDo4
            admin.view_patient(discharged_patients)

        elif op == '4':
            # 4- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors)

        elif op == '5':
            #5 - Reallocated Doctor to Patient with the same function
            admin.reallocate_doctor_to_patient(patients , doctors)

        elif op == '6':
            #6 - View Management Report
            admin.management_reports(doctors , patients)
        elif op == '7':
            # 7- Update admin detais
            admin.update_details()
        elif op == '8':
            admin.view_grouped_patients_by_family(grouped_patients)
        elif op == '9':   # or any free number
            print("\nMake new appointment (admin only)")
            doctor = input("Doctor full name : ").strip()
            patient = input("Patient full name: ").strip()
            date    = input("Date (YYYY-MM-DD): ").strip()
            time    = input("Time (HH:MM)     : ").strip()
            reason  = input("Reason (optional): ").strip()

            if doctor and patient and date and time:
                save_appointment(doctor, patient, date, time, reason)
                print("Appointment saved.")
            else:
                print("Required fields missing.")
        elif op == '10':
            # 8 - Quit
            #ToDo5
            print("Exited Successfully !")
            break

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()
