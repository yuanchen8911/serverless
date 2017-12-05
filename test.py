from items import Item
from shoppingCart import Cart

item1 = Item('a',1,2)
item2 = Item('b',2,3)
c = Cart()
c.addToCart(item1)
c.addToCart(item2)
c.addToCart(item1)
c.removeItem('a')
c.printCart()
c.getTotal()