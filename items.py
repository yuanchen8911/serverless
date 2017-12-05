
class Item(self):
	def __init__(self,name):
		self.ItemName = name
		self.price = 10
		self.unit = 'pound'
		self.quantity = 0
	def setUnit(self,unit):
		self.unit = unit
	def getUnit(self):
		return self.unit
	def setQuantity(self,quantity):
		self.quantity = quantity
	def getQuantity(self):
		return self.quantity

	
