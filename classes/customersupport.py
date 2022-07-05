import classes.baseform as baseform

class customer_support(baseform.baseform):

    def __init__(self, name, reasons, email, description):
        super().__init__(name, reasons)
        self.__customer_support_id = None
        self.__email = email
        self.__description = description
        self.__reply = None

    def get_customer_support_id(self):
        return self.__customer_support_id

    def get_email(self):
        return self.__email

    def get_description(self):
        return self.__description

    def get_reply(self):
        return self.__reply

    def set_customer_support_id(self, customer_support_id):
        self.__customer_support_id = customer_support_id

    def set_email(self, email):
        self.__email = email

    def set_description(self, description):
        self.__description = description

    def set_reply(self, reply):
        self.__reply = reply
