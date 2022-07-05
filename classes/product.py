class Product:

    def __init__(self, name, price, stock, description):
        self.__product_id = None
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__description = description
        self.__imagepath = None

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_description(self):
        return self.__description

    def get_imagepath(self):
        return self.__imagepath

    def set_imagepath(self,imagepath):
        self.__imagepath = imagepath

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_stock(self, stock):
        self.__stock = stock

    def set_description(self, description):
        self.__description = description
