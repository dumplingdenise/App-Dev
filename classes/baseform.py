class baseform:

    def __init__(self,name, reasons):
        self.__name = name
        self.__reasons = reasons

    def get_name(self):
        return self.__name

    def get_reasons(self):
        return self.__reasons

    def set_name(self, name):
        self.__name = name

    def set_reasons(self, reasons):
        self.__reasons = reasons



