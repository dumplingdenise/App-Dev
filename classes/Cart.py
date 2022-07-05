import classes.product as Product


class Cart(Product.Product):
    count = 0

    def __init__(self, name, price, stock, description, quantity):
        super().__init__(name, price, stock, description)
        Cart.count += 1
        self.__quantity = quantity

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity
