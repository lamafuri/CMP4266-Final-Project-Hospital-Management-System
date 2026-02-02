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

    def get_doctor(self) :
        #ToDo3
        return self.__doctor
    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    def print_symptoms(self):
        """prints all the symptoms"""
        #ToDo4

        pass
    # For saving to a text file
    def to_csv_format(self):
        """First Name , Surname , Age , Mobile , Post Code , Doctor , symptom 1|symptom 2|symptom 3"""
        return f"{self.get_first_name()},{self.get_surname()},{self.age},{self.mobile},{self.postcode},{self.__doctor}"

    def __str__(self):
        return f'{self.full_name():^30}|{self.__doctor:^30}|{self.age:^5}|{self.mobile:^15}|{self.postcode:^10}'
