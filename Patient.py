from Person import Person
class Patient(Person):
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, postcode):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            address (string): address
        """

        #ToDo1
        super().__init__(first_name , surname)
        self.age = age
        self.mobile = mobile
        self.postcode = postcode
        self.__doctor = 'None'
        self.__symptoms = []

    def get_doctor(self) :
        #ToDo3
        return self.__doctor
    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor
    def add_symptom(self, symptom):
        if symptom.strip():
            self.__symptoms.append(symptom.strip())
    def get_symptoms(self):
        return self.__symptoms.copy()
    def print_symptoms(self):
        """prints all the symptoms"""
        #ToDo4
        if not self.__symptoms:
            print("  No symptoms recorded.")
        else:
            print("  Symptoms:")
            for i, s in enumerate(self.__symptoms, 1):
                print(f"    {i}. {s}")

        pass
    # For saving to a text file
    def to_csv_format(self):
        """First Name , Surname , Age , Mobile , Post Code , Doctor , symptom 1|symptom 2|symptom 3"""
        symptoms_str = '|'.join(self.__symptoms) if self.__symptoms else ''
        return f"{self.get_first_name()},{self.get_surname()},{self.age},{self.mobile},{self.postcode},{self.__doctor},{symptoms_str}"

    def __str__(self):
        symptoms_part = f"{', '.join(self.__symptoms)}" if self.__symptoms else ""
        return f'{self.full_name():^30}|{self.__doctor:^30}|{self.age:^5}|{self.mobile:^15}|{self.postcode:^10}|{symptoms_part}'
 