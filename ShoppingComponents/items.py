class Item():
    def __init__(self, name, quantity=1, price=10):
        self.itemName = name
        self.price = price
        self.unit = 'pound'
        self.quantity = quantity

    def setUnit(self, unit):
        self.unit = unit

    def getUnit(self):
        return self.unit

    def setQuantity(self, quantity):
        self.quantity = quantity

    def getQuantity(self):
        return self.quantity

    def toString(self):
        str = self.name + " " + str(self.quantity)
        return str

    def getPrice(self):
        return self.price
