# Shopping Bot CUI
## Overview 
A shopping CUI that allows the user adding/removing items toward a shopping cart, reviewing and checking out shopping cart. 
## Features

* Add certain amount of items to shopping cart.
* Remove certain amount of items from shopping cart.
* List current status of the shopping cart.
* checkout items from shopping cart.
* Debug Mode

## Dependencies (Install required Python packages)
> sudo pip install apiai

> sudo pip install termcolor
## Running example 
start the program 
> python ShoppingBot.py

add to cart
> add two apples

remove from cart
> delete two apples

list status
> show me the cart

checkout 
> that's it, check out!

greeting
> What's up 

Enter Debug Mode
> python ShoppingBot.py --debug
## List of Available Products (Common groceries can be found at store.)
#### Our database contains around 2000 items, some of them are less commonly seen, here are some common ones.The full list of items is in Grocery/prices.txt
"sushi" -> "california roll sushi"

"alaskan cod" -> "mulit grain alaskan cod"

"apple" -> "organic honeycrisp apple"

"lemons" -> "organic lemons"

"chicharrones" -> "hot n spicy chicharrones"

"trouts" -> "smoked rainbow trout"

## Synonyms Data Preparation and Matching
1. Preprocess the given items (https://www.instacart.com/datasets/grocery-shopping-2017)
2. Establish synonym connections between potential search items with products names stored in database.

## Logic flow 
### checkout and greetings
![](https://github.com/wwyiyi/95729cui/blob/master/images/1.png)
### adding and remove items
![](https://github.com/wwyiyi/95729cui/blob/master/images/3.png)
### List of Intents
* addToCart
* checkOut
* greeting
* itemCount
* removeFromCart
### List of Entities
* apples
* pear
* and many more 
