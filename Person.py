class Person:
    """Person Class as parent for all other classes : Patient , Doctor"""
    def __init__(self , first_name , surname ):
        self.__first_name = first_name
        self.__surname = surname
    
    def full_name(self) :
        #ToDo1
        return f"{self.__first_name} {self.__surname}"

    def get_first_name(self) :
        #ToDo2
        return self.__first_name

    def set_first_name(self, new_first_name):
        #ToDo3
        self.__first_name = new_first_name
    def get_surname(self) :
        #ToDo4
        return self.__surname

    def set_surname(self, new_surname):
        #ToDo5
        self.__surname = new_surname
    
