import classes.Base as Base

class Order(Base.Base):

    def __init__(self, created_by, first_name, last_name, contact_no, email, address, notes, cdname, ccnum, exp_mth, exp_yr, ccv ):
        super().__init__(created_by)
        self.__order_id = None
        self.__first_name = first_name
        self.__last_name = last_name
        self.__contact_no = contact_no
        self.__email = email
        self.__address = address
        self.__notes = notes
        self.__cdname = cdname
        self.__ccnum = ccnum
        self.__exp_mth = exp_mth
        self.__exp_yr = exp_yr
        self.__ccv = ccv


    def get_order_id(self):
        return self.__order_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_contact_no(self):
        return self.__contact_no

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_notes(self):
        return self.__notes

    def get_cdname(self):
        return self.__cdname

    def get_ccnum(self):
        return self.__ccnum

    def get_exp_mth(self):
        return self.__exp_mth

    def get_exp_yr(self):
        return self.__exp_yr

    def get_ccv(self):
        return self.__ccv

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_contact_no(self, contact_no):
        self.__contact_no = contact_no

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_notes(self, notes):
        self.__notes = notes

    def set_cdname(self, cdname):
        self.__cdname = cdname

    def set_ccnum(self, ccnum):
        self.__ccnum = ccnum

    def set_exp_mth(self, exp_mth):
        self.__exp_mth = exp_mth

    def set_exp_yr(self, exp_yr):
        self.__exp_yr = exp_yr

    def set_ccv(self, ccv):
        self.__ccv = ccv
