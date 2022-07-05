import datetime


class Base:
    def __init__(self, created_by):
        self.__created_by = created_by
        self.__modified_by = None
        self.__date_created = datetime.datetime.now()
        self.__date_modified = None

    def get_created_by(self):
        return self.__created_by

    def get_modified_by(self):
        return self.__modified_by

    def get_date_created(self):
        return self.__date_created

    def get_date_modified(self):
        return self.__date_modified

    def set_created_by(self, created_by):
        self.__created_by = created_by

    def set_modified_by(self, modified_by):
        self.__modified_by = modified_by

    def set_date_modified(self):
        date_modified = datetime.datetime.now()
        self.__date_modified = date_modified
