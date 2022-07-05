import Users.User

class Staff(Users.User.User):
    count_id = 0

    def __init__(self, first_name, last_name, role, username, email, contact, password, cfmpw):
        super().__init__(first_name, last_name)
        Staff.count_id += 1
        self.__Staff_id = Staff.count_id
        self.__role = role
        self.__username = username
        self.__email = email
        self.__contact = contact
        self.__password = password
        self.__cfmpw = cfmpw

    def get_Staff_id(self):
        return self.__Staff_id

    def get_role(self):
        return self.__role

    def get_email(self):
        return self.__email

    def get_username(self):
        return self.__username

    def get_contact(self):
        return self.__contact

    def get_password(self):
        return self.__password

    def get_cfmpw(self):
        return self.__cfmpw

    def set_Staff_id(self, Staff_id):
        self.__Staff_id = Staff_id

    def set_role(self, role):
        self.__role = role

    def set_email(self, email):
        self.__email = email

    def set_username(self, username):
        self.__username = username

    def set_contact(self, contact):
        self.__contact = contact

    def set_password(self, password):
        self.__password = password

    def set_cfmpw(self, cfmpw):
        self.__cfmpw = cfmpw


