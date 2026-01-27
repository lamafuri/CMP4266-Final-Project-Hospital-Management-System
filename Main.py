# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
from utility_functions import load_doctors_data , load_patients_data , load_discharged_patients_data
def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors
    admin = Admin('admin','123','B1 1AB') # username is 'admin', password is '123'
    # doctors = [Doctor('John','Smith','Internal Med.'), Doctor('Jone','Smith','Pediatrics'), Doctor('Jone','Carlos','Cardiology')]
    doctors = load_doctors_data()
    # patients = [Patient('Sara','Smith', 20, '07012345678','B1 234'), Patient('Mike','Jones', 37,'07555551234','L2 2AB'), Patient('Daivd','Smith', 15, '07123456789','C1 ABC')]
    patients , grouped_patients = load_patients_data()
    # discharged_patients = []
    discharged_patients = load_discharged_patients_data()

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
        print(' 5- Update admin detais')
        print(' 6- Quit')

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
            # 5- Update admin detais
            admin.update_details()

        elif op == '6':
            # 6 - Quit
            #ToDo5
            print("Exited Successfully !")
            break

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()
