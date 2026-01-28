from Doctor import Doctor
from utility_functions import update_file
from Patient import Patient


class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, address = ''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self.__address =  address

    def view(self,a_list):
        """
        print a list
        Args:
            a_list (list): a list of printables
        """

        for index, item in enumerate(a_list):
            print(f'{index+1:<3}|{item}')

    def login(self) :
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password don`t match the data registered
        Returns:
            string: the username
        """
    
        print("-----Login-----")
        #Get the details of the admin

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # check if the username and password match the registered ones
        #ToDo1
        if(self.__username == username and self.__password == password):
            return self.__username
        else:
            raise Exception("incorrect username or password")

    def find_index(self,index,doctors):
        # check that the doctor id exists          
        if index in range(0,len(doctors)):
            return True
        # if the id is not in the list of doctors
        else:
            return False
            
    def get_doctor_details(self) :
        """
        Get the details needed to add a doctor
        Returns:
            first name, surname and the speciality of the doctor in that order.
        """
        #ToDo2
        first_name = input("Enter the doctor's first name : ")
        surname = input("Enter the doctor surname : ")
        speciality = input("Enter the doctor speciality : ")
        return first_name , surname , speciality

    def doctor_management(self, doctors):
        """
        A method that deals with registering, viewing, updating, deleting doctors
        Args:
            doctors (list<Doctor>): the list of all the doctors names
        """

        print("-----Doctor Management-----")

        # menu
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')

        #ToDo3
        op = input('Input: ')

        # register
        if op == '1':
            print("-----Register-----")

            # get the doctor details
            print('Enter the doctor\'s details:')
            #ToDo4
            first_name , surname , speciality = self.get_doctor_details()

            # check if the name is already registered
            name_exists = False
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')
                    #ToDo5
                    name_exists = True
                    break # save time and end the loop

            #ToDo6
            if(not name_exists):
                new_doctor = Doctor(first_name , surname , speciality)
                try:
                    with open('./Data/doctor.txt' ,'a') as file:
                        file.write(new_doctor.to_csv_format()+'\n')
                except Exception as e:
                    print("Error appending new doctor to doctor.txt \nError: ",e)
                else:
                    doctors.append(new_doctor) # add the doctor to the list of doctors
                    print('Doctor registered.')
                

        # View
        elif op == '2':
            print("-----List of Doctors-----")
            #ToDo7
            print('ID |          Full name           |  Speciality') #3 ,30 ,12
            self.view(doctors)

        # Update
        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name           |  Speciality') #3 ,30 ,12
                self.view(doctors)
                try:
                    index = int(input('Enter the ID of the doctor to be updated : ')) - 1
                    doctor_index=self.find_index(index,doctors)
                    if doctor_index!=False:
                        break  
                    else:
                        print("Doctor not found")

                    
                        # doctor_index is the ID mines one (-1)
                        

                except ValueError: # the entered id could not be changed into an int
                    print('The ID entered is incorrect')

            # menu
            print('Choose the field to be updated:')
            print(' 1 First name')
            print(' 2 Surname')
            print(' 3 Speciality')
            op = input('Input: ') # make the user input lowercase

            #ToDo8
            if op == '1':
                new_first_name = input("Enter the new first name: ")
                doctors[index].set_first_name(new_first_name)
            elif op == '2':
                new_surname = input("Enter the new surname: ")
                doctors[index].set_surname(new_surname)
            elif op == '3':
                new_speciality = input("Enter the new speciality: ")
                doctors[index].set_speciality(new_speciality)
            else:
                print("Invalid operation choosen ! Check Spelling")
            update_file(doctors , 'doctor.txt')

        # Delete
        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)
            
            doctor_index = input('Enter the ID of the doctor to be deleted: ')
            #ToDo9
            if (self.find_index(doctor_index)):
                doctors.pop(doctor_index)
                print("Doctor deleted")
            else:
                print('The id entered was not found')
            
            update_file(doctors , 'doctor.txt')


        else:
            print('Invalid operation choosen. Check your spelling!')

    def admit_patient(self , patients):
        print("------- Admit Patient -------")
        print("Enter Patient's Details")
        first_name = input("Enter patient's first name: ")
        surname = input("Enter patient's surname: ")
        age = int(input("Enter the patient's age: "))
        mobile = input("Enter the patient's mobile number: ")
        postcode = input("Enter the patient's address post code: ")
        new_patient = Patient(first_name , surname , age , mobile , postcode)
        patients.append(new_patient)
        update_file(patients ,'patient.txt')

    def view_patient(self, patients):
        """
        print a list of patients
        Args:
            patients (list<Patients>): list of all the active patients
        """
        print("-----View Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        #ToDo10
        self.view(patients)

    def assign_doctor_to_patient(self, patients, doctors):
        """
        Allow the admin to assign a doctor to a patient
        Args:
            patients (list<Patients>): the list of all the active patients
            doctors (list<Doctor>): the list of all the doctors
        """
        print("-----Assign-----")

        print("-----Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        self.view(patients)

        patient_index = input('Please enter the patient ID: ')

        try:
            # patient_index is the patient ID mines one (-1)
            patient_index = int(patient_index) -1

            # check if the id is not in the list of patients
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return # stop the procedures

        except ValueError: # the entered id could not be changed into an int
            print('The id entered is incorrect')
            return # stop the procedures

        print("-----Doctors Select-----")
        print('Select the doctor that fits these symptoms:')
        patients[patient_index].print_symptoms() # print the patient symptoms

        print('--------------------------------------------------')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)
        doctor_index = input('Please enter the doctor ID: ')

        try:
            # doctor_index is the patient ID mines one (-1)
            doctor_index = int(doctor_index) -1

            # check if the id is in the list of doctors
            if self.find_index(doctor_index,doctors)!=False:
                    
                # link the patients to the doctor and vice versa
                #ToDo11
                patients[patient_index].link(doctors[doctor_index].full_name())
                doctors[doctor_index].add_patient(patients[patient_index])                
                print('The patient is now assign to the doctor.')
                update_file(patients , 'patient.txt')

            # if the id is not in the list of doctors
            else:
                print('The id entered for doctor was not found.')

        except ValueError: # the entered id could not be changed into an in
            print('The id entered is incorrect')

    def reallocate_doctor_to_patient(self, patients, doctors):
        """
        Allow the admin to reallocate a new doctor to a patient
        Args:
            patients (list<Patients>): the list of all the active patients
            doctors (list<Doctor>): the list of all the doctors
        """
        print("-----Reallocate new Doctor to Patient-----")

        print("-----Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        self.view(patients)

        patient_index = input('Please enter the patient ID whose doctor is to be changed: ')

        try:
            # patient_index is the patient ID mines one (-1)
            patient_index = int(patient_index) -1

            # check if the id is not in the list of patients
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return # stop the procedures

        except ValueError: # the entered id could not be changed into an int
            print('The id entered is incorrect')
            return # stop the procedures

        print("-----Select new Doctor-----")
        print('Select new doctor that fits these symptoms:')
        patients[patient_index].print_symptoms() # print the patient symptoms

        print('--------------------------------------------------')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)
        doctor_index = input('Please enter the new doctor ID: ')

        try:
            # doctor_index is the patient ID mines one (-1)
            doctor_index = int(doctor_index) -1

            # check if the id is in the list of doctors
            if self.find_index(doctor_index,doctors)!=False:
                    
                # link the patients to the doctor and vice versa
                #ToDo11
                previous_doctor_name = patients[patient_index].get_doctor()
                
                for doctor in doctors:
                    if doctor.full_name() == previous_doctor_name:
                        previous_doctor = doctor
                        previous_doctor.remove_patient(patients[patient_index])
                        break
                patients[patient_index].link(doctors[doctor_index].full_name())
                doctors[doctor_index].add_patient(patients[patient_index])

                update_file(patients , 'patient.txt')

            # if the id is not in the list of doctors
            else:
                print('The id entered for doctor was not found.')

        except ValueError: # the entered id could not be changed into an in
            print('The id entered is incorrect')

    def discharge(self, patients, discharged_patients):
        """
        Allow the admin to discharge a patient when treatment is done
        Args:
            patients (list<Patients>): the list of all the active patients
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        print("-----Discharge Patient-----")

        patient_index = input('Please enter the patient ID: ')

        #ToDo12
        try:
            patient_index = int(patient_index)-1;
        except ValueError as e:
            print("Invalid input! Please enter a valid ID")
        else:
            discharged_one = patients.pop(patient_index)
            discharged_patients.append(discharged_one)
            update_file(patients , 'patient.txt')
            update_file(discharged_patients , 'discharged_patient.txt')
            print(f"{discharged_one.full_name()} was discharged")

    def view_discharge(self, discharged_patients):
        """
        Prints the list of all discharged patients
        Args:
            discharge_patients (list<Patients>): the list of all the non-active patients
        """

        print("-----Discharged Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        #ToDo13
        self.view(discharged_patients)
    
    def update_details(self):
        """
        Allows the user to update and change username, password and address
        """

        print('Choose the field to be updated:')
        print(' 1 Username')
        print(' 2 Password')
        print(' 3 Address')
        op = int(input('Input: '))

        if op == 1:
            #ToDo14
            new_username = input("Enter new username: ")
            self.__username = new_username

        elif op == 2:
            password = input('Enter the new password: ')
            # validate the password
            if password == input('Enter the new password again: '):
                self.__password = password

        elif op == 3:
            #ToDo15
            new_address = input("Enter new address: ")
            self.__address = new_address

        else:
            #ToDo16
            print("Invalid operation! Please enter a valid operation")

    def management_reports(self , doctors):
        print("\t1. View total number of Doctors")
        print("\t2. View total number of Patients per Doctor")
        print("\t3. View total number of appointments per Dcotor")
        print("\t4. View total number of Patients based on illness types")
        op = input("Enter the operation (1,2,3,4): ")
        if(op == '1'):
            print("Total Number of doctor : ",len(doctors))
        elif op == '2':
            print("-----Total Number of Patient's per Doctor-----")
            for doctor in doctors:
                print(f"\t{doctor.full_name()} has : {len(doctor.get_patients())} patients")
        elif op == '3':
            # appointent per doctor
            pass
        elif op == '4':
            # Patient based on illness
            pass
        else:
            print("Ivalid Input ! Enter 1 ,2 ,3 or 4")

if __name__ =='__main__': 
    my = Admin('a','123','salleri')
    my.doctor_management([Doctor("Furi","Lama","Surgeon")])
    # my.view_patient([Patient("Furi","Lama",18, "9749214495","22334")])
    # my.assign_doctor_to_patient([Patient("Furi","Lama",18, "9749214495","22334")] ,[Doctor("Furi","Lama","Surgeon")] )
    # my.discharge([Patient("Furi","Lama",18, "9749214495","22334")] , [])
    # my.update_details()

