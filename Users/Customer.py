import Users.User

class Customer(Users.User.User):
    count_id = 0

    def __init__(self, first_name, last_name, email, contact, password, cfmpw):
        super().__init__(first_name, last_name)
        Customer.count_id += 1
        self.__Customer_id = Customer.count_id
        self.__email = email
        self.__contact = contact
        self.__password = password
        self.__cfmpw = cfmpw

    def get_Customer_id(self):
        return self.__Customer_id

    def get_email(self):
        return self.__email

    def get_contact(self):
        return self.__contact

    def get_password(self):
        return self.__password

    def get_cfmpw(self):
        return self.__cfmpw

    def set_Customer_id(self, Customer_id):
        self.__Customer_id = Customer_id

    def set_email(self, email):
        self.__email = email

    def set_contact(self, contact):
        self.__contact = contact

    def set_password(self, password):
        self.__password = password

    def set_cfmpw(self, cfmpw):
        self.__cfmpw = cfmpw
