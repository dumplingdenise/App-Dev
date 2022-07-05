import classes.product as Product


class Toy(Product.Product):

    def __init__(self, name, price, stock, description, agegroup):
        super().__init__(name, price, stock, description)
        self.__agegroup = agegroup

    def set_agegroup(self, agegroup):
        self.__agegroup = agegroup

    def get_agegroup(self):
        return self.__agegroup


#lol = Toy('name',2.4,300,'yes', 2)
#print(lol.get_agegroup())